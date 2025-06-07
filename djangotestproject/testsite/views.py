from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Transaction, Category
from django.db.models import Sum, Case, When, DecimalField, Q


panel = [
    {'title': 'Main', 'name': 'home'},
    {'title': 'About', 'name': 'about'},
    {'title': 'Contact', 'name': 'contact'},
    {'title':'Login', 'name': 'login'}
]

CURRENCY_INFO = {
    'USD': {'symbol': '$', 'flag': '🇺🇸'},
    'EUR': {'symbol': '€', 'flag': '🇪🇺'},
    'GBP': {'symbol': '£', 'flag': '🇬🇧'},
    'JPY': {'symbol': '¥', 'flag': '🇯🇵'},
    'RUB': {'symbol': '₽', 'flag': '🇷🇺'},
    'CNY': {'symbol': '¥', 'flag': '🇨🇳'},
    'CHF': {'symbol': 'kr', 'flag': '🇨🇭'},
    'UAH': {'symbol': '₴', 'flag': '🇺🇦'},
    'PLN': {'symbol': 'zł', 'flag': '🇵🇱'},
    'CAD': {'symbol': 'C$', 'flag': '🇨🇦'},
    'AUD': {'symbol': 'A$', 'flag': '🇦🇺'},
}


def exchange_rates(request):
    try:
        url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=6415fb4702ca403b9914a13de347826d&symbols=UAH,PLN,EUR,GBP,CAD,AUD,JPY,CNY,CHF,RUB"
        response = requests.get(url)
        data = response.json()

        raw_rates = data.get('rates', {})
        rates = []

        for code, rate in raw_rates.items():
            info = CURRENCY_INFO.get(code, {})
            rates.append({
                'code': code,
                'rate': rate,
                'symbol': info.get('symbol', ''),
                'flag': info.get('flag', ''),
            })

        context = {
            'base': data.get('base', 'USD'),
            'date': data.get('date'),
            'rates': rates,
        }

    except Exception as e:
        context = {'error': f'Ошибка при получении данных: {e}'}

    return render(request, 'testsite/exchange_rates.html', context)

def about(request):
    inform = {'panel': panel}
    return render(request, 'testsite/about.html', context=inform)


@login_required()
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('cat')
    data = {
        'transactions': transactions
    }
    return render(request, 'testsite/transaction_list.html', context=data)

@login_required()
def category(request):
    categories = Category.objects.filter(Q(user=None) | Q(user=request.user))
    data = {
        'categories': categories
    }
    return render(request, 'testsite/category.html', context=data)


@login_required()
def statistic_view(request):

    total = Transaction.objects.filter(user=request.user).aggregate(
        total_in=Sum(Case(When(transaction_type='income', then='amount'), output_field=DecimalField())),
        total_ex=Sum(Case(When(transaction_type='expense', then='amount'), output_field=DecimalField()))
    )

    category_stats = (
        Transaction.objects.filter(user=request.user)
        .values('cat__name')
        .annotate(
            cat_in=Sum(Case(When(transaction_type='income', then='amount'), output_field=DecimalField())),
            cat_ex=Sum(Case(When(transaction_type='expense', then='amount'), output_field=DecimalField()))
        )
    )

    for stat in category_stats:
        stat['total_cat_sum'] = (stat['cat_in'] or 0) - (stat['cat_ex'] or 0)

    data = {
        'total_in': total['total_in'] or 0,
        'total_ex': total['total_ex'] or 0,
        'total_sum': (total['total_in'] or 0) - (total['total_ex'] or 0),
        'cat_stat': category_stats,
    }

    return render(request, 'testsite/statistic.html', context=data)


class TransAdd(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['amount', 'transaction_type', 'cat']
    template_name = 'testsite/add_new.html'
    success_url = reverse_lazy('transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] = 'Add new transaction'
        return context

    def form_valid(self, form):
        cat = form.cleaned_data['cat']
        if cat.user is not None and cat.user != self.request.user:
            form.add_error('cat', 'Incorrect category')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cat'].queryset = Category.objects.filter(Q(user=None) | Q(user=self.request.user))
        return form


class TransUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['amount', 'transaction_type', 'cat']
    template_name = 'testsite/add_new.html'
    success_url = reverse_lazy('transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] =  'Transaction update'
        return context

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        cat = form.cleaned_data['cat']
        if cat.user is not None and cat.user != self.request.user:
            form.add_error('cat', 'Incorrect category')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cat'].queryset = Category.objects.filter(Q(user=None) | Q(user=self.request.user))
        return form


class TransDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'testsite/delete.html'
    success_url = reverse_lazy('transaction')  # куда перенаправлять после удаления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] = 'Delete transaction'
        return context

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class CategoryAdd(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'testsite/add_new.html'
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Add new category'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdate(LoginRequiredMixin, UpdateView):
     model = Category
     fields = ['name', 'description']
     template_name = 'testsite/add_new.html'
     success_url = reverse_lazy('category')

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Update category'
        return context

     def get_queryset(self):
         return Category.objects.filter(user=self.request.user)


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'testsite/delete.html'
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Delete category'
        return context

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

def page_not_found(request, exception):
    return render(request, 'errors/error404.html', status=404)