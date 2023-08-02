from django.urls import path, re_path
from .views import home_view, access_grades, course_view, course_detail, filtered_content, plan_details, pay, handle_transaction
from . import views


app_name = 'website_content'
urlpatterns = [
    path('home/', home_view, name='home'),
    path('home/<str:name>/', course_detail, name='course_detail'),
    path('home/<str:name>/<str:slug>/',
         filtered_content, name='filtered_content'),
    path('plan/', plan_details, name='plan_details'),
    path('pay/<str:price>/', pay, name='pay'),
    path('handle-transaction/<str:price>/',
         handle_transaction, name='handle_transaction'),
    path('access_grades/', access_grades, name='access_grades'),
    path('course/<slug:slug>/', course_view, name='course_view'),
]
