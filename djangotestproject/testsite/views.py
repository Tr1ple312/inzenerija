from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Transaction, Category
from django.db.models import Sum, Case, When, DecimalField


panel = [
    {'title': 'Main', 'name': 'home'},
    {'title': 'About', 'name': 'about'},
    {'title': 'Contact', 'name': 'contact'},
    {'title':'Login', 'name': 'login'}
]


def about(request):
    inform = {'panel': panel}
    return render(request, 'testsite/about.html', context=inform)


def contact(request):
    return HttpResponse('this is contact page')


def login(request):
    return HttpResponse('this is login page')


def dynamic(request, id):
    return HttpResponse(f'id = {id}')


def transaction_list(request):
    transactions = Transaction.objects.all().select_related('cat')
    data = {
        'transactions': transactions
    }
    return render(request, 'testsite/transaction_list.html', context=data)


def category(request):
    categories = Category.objects.all()
    data = {
        'categories': categories
    }
    return render(request, 'testsite/category.html', context=data)


def statistic_view(request):

    total = Transaction.objects.aggregate(
        total_in=Sum(Case(When(transaction_type='income', then='amount'), output_field=DecimalField())),
        total_ex=Sum(Case(When(transaction_type='expense', then='amount'), output_field=DecimalField()))
    )

    category_stats = (
        Transaction.objects.values('cat__name')
        .annotate(
            cat_in=Sum(Case(When(transaction_type='income', then='amount'), output_field=DecimalField())),
            cat_ex=Sum(Case(When(transaction_type='expense', then='amount'), output_field=DecimalField()))
        )
    )

    # Добавляем вычисляемое поле
    for stat in category_stats:
        stat['total_cat_sum'] = (stat['cat_in'] or 0) - (stat['cat_ex'] or 0)

    data = {
        'total_in': total['total_in'] or 0,
        'total_ex': total['total_ex'] or 0,
        'total_sum': (total['total_in'] or 0) - (total['total_ex'] or 0),
        'cat_stat': category_stats,
    }

    return render(request, 'testsite/statistic.html', context=data)


class TransAdd(CreateView):
    model = Transaction
    fields = ['amount', 'transaction_type', 'cat']
    template_name = 'testsite/add_new.html'
    success_url = reverse_lazy('transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] = 'Add new transaction'
        return context


class TransUpdate(UpdateView):
    model = Transaction
    fields = ['amount', 'transaction_type', 'cat']
    template_name = 'testsite/add_new.html'
    success_url = reverse_lazy('transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] =  'Transaction update'
        return context


class TransDelete(DeleteView):
    model = Transaction
    template_name = 'testsite/delete.html'
    success_url = reverse_lazy('transaction')  # куда перенаправлять после удаления

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'transaction'
        context['title'] = 'Delete transaction'
        return context


class CategoryAdd(CreateView):
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


class CategoryUpdate(UpdateView):
     model = Category
     fields = ['name', 'description']
     template_name = 'testsite/add_new.html'
     success_url = reverse_lazy('category')

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Update category'
        return context


class CategoryDelete(DeleteView):
    model = Category
    template_name = 'testsite/delete.html'
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'category'
        context['title'] = 'Delete category'
        return context


def page_not_found(request, exception):
    return render(request, 'errors/error404.html', status=404)