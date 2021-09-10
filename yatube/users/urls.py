from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)
from django.urls import path
from . import views


app_name = 'users'
reset_password = 'users/password_reset_form.html'
reset_password_done = 'users/password_reset_done.html'
change_password = 'users/password_change_form.html'
change_password_done = 'users/password_change_done.html'
urlpatterns = [
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup',
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name=reset_password),
        name='password_reset_form',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name=reset_password_done),
        name='password_reset_done',
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name=change_password),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name=change_password_done),
        name='password_change_done',
    )
]
