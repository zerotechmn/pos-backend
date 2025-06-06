from django.contrib.auth import views
from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,)

from front.login.forms import LoginForm
from django.http import HttpResponseRedirect

class FrontLoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'login/login.html'


class FrontLogoutView(views.LogoutView):
    template_name = 'login/logout.html'