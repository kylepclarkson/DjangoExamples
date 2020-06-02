from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Replaced by using Django's login view
    # path('login/', views.user_login, name='login')
    # login/logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # dashboard
    path('', views.dashboard, name='dashboard'),
    # change password urls
    # path('password_change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change_done'),
    # # reset password urls
    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password_reset/done',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_complete'),
    # Since we're using Django's views, we can map all urls using the below.
    path('', include('django.contrib.auth.urls'))
]