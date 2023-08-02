# course.urls.py
from django.urls import path
from .views import COURSES, course_detail, filtered_content


app_name = 'course'

urlpatterns = [
    # Updated name from 'Courses' to 'course_list'
    path('', COURSES, name='course_list'),
    path('<str:name>/', course_detail, name='course_detail'),
    path('<str:name>/<str:slug>/', filtered_content, name='filtered_content'),

]
