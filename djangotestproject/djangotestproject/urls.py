from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('testsite.urls')),
    path("users/", include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),

]

handler403 = 'testsite.views.permission_denied'
handler404 = 'testsite.views.page_not_found'
handler500 = 'testsite.views.server_error'


