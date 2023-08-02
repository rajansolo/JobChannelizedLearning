from django.urls import path, re_path
from . import views

app_name = 'user_account'
urlpatterns = [
    path('', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('you_have_to_logout_first/', views.you_have_to_logout_first, name='you_have_to_logout_first'),
    path('register/', views.user_registration_view, name='register'),
    path('login_first/', views.login_first, name='login_first'),
    path('registration_successful/', views.registration_successful_view, name='registration_successful'),
]
