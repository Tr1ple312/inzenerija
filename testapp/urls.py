from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('testsite.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

]

handler404 = 'testsite.views.page_not_found'  # Обработчик ошибки 404
