from django.http import HttpResponse
from django.shortcuts import render

from .models import Transaction, Category
from django.db.models import Sum


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
    transactions = Transaction.objects.all()
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
    total_ex = Transaction.objects.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total']
    total_in = Transaction.objects.filter(transaction_type='income').aggregate(total=Sum('amount'))['total']
    data = {
        'total_ex': total_ex,
        'total_in': total_in
    }
    return render(request, 'testsite/statistic.html', context=data)


def page_not_found(request, exception):
    return render(request, 'errors/error404.html', status=404)