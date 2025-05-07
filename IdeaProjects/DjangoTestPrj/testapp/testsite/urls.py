from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction'),
    path('about/', views.about, name='about'),
    path('id/<int:id>/', views.dynamic, name='dynamic_page'),
    path('contact/', views.contact, name='current'),
    path('login/', views.login, name='login'),
    path('category/', views.category, name='category'),
    path('statistic/', views.statistic_view, name='statistic')
]

# TODO: сделать сайдбар
# TODO: стилизация + оптимизация статистики
# TODO: фильтры
# TODO: EDIT, DELETE, NEW функции изменения
# TODO: аторизация
# TODO: current value API
