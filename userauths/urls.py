from django.urls import path, include
from userauths import views,utils

app_name = "userauths"

urlpatterns = [
    path('user/sign-up/', views.register_view, name= "sign-up"),
    path('user/sign-in/', views.login_view, name="sign-in"),
    path('confirm-email/<str:token>/', utils.confirm_email, name='confirm_email'),
    path('email-confirmed/', views.email_confirmed, name="email_confirmed"),
    path('invalid-token/', views.email_invalid, name="invalid_token"),
    path('reset-password/<str:token>/', views.password_reset_form, name='password_reset_form'),
    path('process-password-reset/', views.process_password_reset, name='process_password_reset'),
    path('user/send-password-reset-email/', views.send_password_reset, name='send-password-reset-email'),
    path('password-reset-success/', views.password_reset_success, name="password-reset-success"),
    path('password-reset-cooldown/', views.password_reset_cooldown, name='password_reset_cooldown'),
    path('logout', views.logout_view, name="logout"),
]
 
