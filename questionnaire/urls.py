# questionnaire/urls.py
from django.urls import path
from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('', views.questionnaire_view, name='questionnaire_form'),
    path('thanks/', views.thanks_view, name='thanks'),
]
