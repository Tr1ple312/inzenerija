from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from .forms import AddTransForm
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
    # Общие суммы
    total = Transaction.objects.aggregate(
        total_in=Sum(Case(When(transaction_type='income', then='amount'), output_field=DecimalField())),
        total_ex=Sum(Case(When(transaction_type='expense', then='amount'), output_field=DecimalField()))
    )

    # Статистика по категориям
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


def trans_add(request):
    if request.method == 'POST':
        form = AddTransForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем транзакцию в базе данных
            return redirect('transaction')  # Перенаправляем на страницу добавления
    else:
        form = AddTransForm()  # Инициализируем пустую форму при GET-запросе

    data = {'form': form}
    return render(request, 'testsite/transadd.html', context=data)



def page_not_found(request, exception):
    return render(request, 'errors/error404.html', status=404)