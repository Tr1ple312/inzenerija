from django.urls import path

from . import views
from .views import TransDelete, CategoryAdd, CategoryUpdate, CategoryDelete

urlpatterns = [
    path('', views.transaction_list, name='transaction'),
    path('about/', views.about, name='about'),
    path('current/', views.current_val, name='current'),
    path('category/', views.category, name='category'),
    path('statistic/', views.statistic_view, name='statistic'),
    path('transadd/', views.TransAdd.as_view(), name='transaction-add'),
    path('update/<int:pk>', views.TransUpdate.as_view(), name='transaction-update'),
    path('delete/<int:pk>/', TransDelete.as_view(), name='transaction-delete'),
    path('categoryadd/', CategoryAdd.as_view(), name='category-add'),
    path('catupdate/<int:pk>', CategoryUpdate.as_view(), name='category_update'),
    path('catdelete/<int:pk>', CategoryDelete.as_view(), name='category_delete'),
]

# TODO: аторизация
# TODO: проверка вводимых данных
# TODO: current value API
# TODO: изменить кнопки edit/delete в просмотре категорий
# TODO: изменить отображение номера транзакции (с pk на реальный номер)
# TODO: добавить выбор валюты
# TODO: пагинация