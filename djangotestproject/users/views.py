from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import LoginUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
