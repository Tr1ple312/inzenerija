from django.conf.urls import handler400
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('testsite.urls')),

]

handler404 = 'testsite.views.page_not_found'  # Обработчик ошибки 404
