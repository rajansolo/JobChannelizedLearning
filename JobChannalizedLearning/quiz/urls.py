from django.urls import path
from .views import (
    Quiz_list_view,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    quizzes,
    add_quiz,
    update_quiz,
    delete_quiz,
    question_list,
    add_question,
    delete_question,
    update_question,
)

app_name = 'quiz'

urlpatterns = [
    path('quizzes/<str:slug>/', quizzes, name='quizzes'),
    path('add_quiz/<str:slug>/', add_quiz, name='add_quiz'),
    path('update-quiz/<int:quiz_id>/<str:slug>/', update_quiz, name='update_quiz'),
    path('delete-quiz/<int:quiz_id>/<str:slug>/', delete_quiz, name='delete_quiz'),
    path('<str:slug>', Quiz_list_view.as_view(), name='main-view'),
    path('<str:slug>/<int:pk>/', quiz_view, name='quiz-view'),
    path('<str:slug>/<int:pk>/save/', save_quiz_view, name='save-view'),
    path('<str:slug>/<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('update/question-list/<int:quiz_id>/', question_list, name='question_list'),
    path('update/add-question/<int:quiz_id>/', add_question, name='add_question'),
    path('update/delete-question/<int:question_id>/', delete_question, name='delete_question'),
    path('update/update-question/<int:question_id>/', update_question, name='update_question'),
]
