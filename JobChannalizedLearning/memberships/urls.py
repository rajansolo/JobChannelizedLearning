from django.urls import path, re_path
from . import views

app_name = 'membership'
urlpatterns = [
    path('', views.membership_view, name='Select_Membership'),
]