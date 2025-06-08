from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Transaction, Category
from django.db.models import Sum, Case, When, DecimalField, Q
from django.core.paginator import Paginator



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
    cached_data = cache.get('exchange_rates')
    if cached_data:
        context = cached_data
    else:
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
            cache.set('exchange_rates', context, 60 * 60)  # 1 час

        except Exception as e:
            context = {'error': f'Ошибка при получении данных: {e}'}

    return render(request, 'testsite/exchange_rates.html', context)


def about(request):
    inform = {'panel': panel}
    return render(request, 'testsite/about.html', context=inform)


@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

    # Фильтры
    transaction_type = request.GET.get('type')
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if transaction_type in ['income', 'expense']:
        qs = qs.filter(transaction_type=transaction_type)
    if category:
        qs = qs.filter(cat__slug=category)
    if date_from:
        qs = qs.filter(transaction_date__gte=date_from)
    if date_to:
        qs = qs.filter(transaction_date__lte=date_to)

    paginator = Paginator(qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total = paginator.count
    start_index = page_obj.start_index()

    numbered_transactions = []
    for i, transaction in enumerate(page_obj, start=0):
        number = total - (start_index - 1) - i
        numbered_transactions.append((number, transaction))

    context = {
        'numbered_transactions': numbered_transactions,
        'page_obj': page_obj,
        'categories': Category.objects.all()
    }
    return render(request, 'testsite/transaction_list.html', context)


@login_required()
def category(request):
    user = request.user if request.user.is_authenticated else None
    categories = Category.objects.filter(Q(user=None) | Q(user=user))
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
        amount = form.cleaned_data.get('amount')
        if amount < 0:
            form.add_error('amount', 'Transaction amount cannot be negative')
            return self.form_invalid(form)

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

    BASE_CATEGORY_NAMES = [
                            'Other', 'Clothing & Footwear', 'Education', 'Income', 'Utilities',
                            'Travel', 'Entertainment', 'Health', 'Transportation', 'Groceries'
                          ]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Add new category'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        name = form.cleaned_data['name'].lower()

        if name in [n.lower() for n in self.BASE_CATEGORY_NAMES]:
            form.add_error('name', 'You cannot use this category name because it is reserved as a base category.')
            return self.form_invalid(form)

        if Category.objects.filter(name__iexact=name, user=self.request.user).exists():
            form.add_error('name', 'You already have a category with this name.')
            return self.form_invalid(form)

        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        form.instance.slug = slug

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
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 200:
            obj = self.get_object()
            if obj.is_base:
                return HttpResponseForbidden("You cannot edit a base category.")
        return response


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
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 200:
            obj = self.get_object()
            if obj.is_base:
                return HttpResponseForbidden("You cannot edit a base category.")
        return response

def page_not_found(request, exception):
    return render(request, 'errors/error404.html', status=404)

def server_error(request):
    return render(request, 'errors/error500.html', status=500)

def permission_denied(request, exception):
    return render(request, 'errors/error403.html', status=403)
