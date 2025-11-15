from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('create_user_sisu__retool/', views.create_user_retool, name='create_user_retool'),
    path('verify_user', views.verify_user, name='verify_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout, name="logout"),
    path('check_team/', views.check_team, name="check_team"),
    path('check_email/', views.check_email, name="check_email"),
    path('send_confirmation_code/', views.send_confirmation_code, name="send_confirmation_code"),
    path('forgot_password/', views.forgot_password, name="forgot_password")]
