from django.urls import path
from . import views
from .views import TransDelete

urlpatterns = [
    path('', views.transaction_list, name='transaction'),
    path('about/', views.about, name='about'),
    path('id/<int:id>/', views.dynamic, name='dynamic_page'),
    path('contact/', views.contact, name='current'),
    path('login/', views.login, name='login'),
    path('category/', views.category, name='category'),
    path('statistic/', views.statistic_view, name='statistic'),
    path('transadd/', views.TransAdd.as_view(), name='transaction-add'),
    path('update/<int:pk>', views.TransUpdate.as_view(), name='transaction-update'),
    path('delete/<int:pk>/', TransDelete.as_view(), name='transaction-delete'),

]

# TODO: аторизация
# TODO: current value API
# TODO: фильтры
