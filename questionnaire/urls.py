from django.urls import path
from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('', views.questionnaire_create, name='questionnaire_form'),
    path('thanks/', views.thanks, name='thanks'),
    path('list/', views.patient_list, name='patient_list'),
    path('export/csv/', views.export_patients_csv, name='export_csv'),
    path('export/pdf/', views.export_patients_pdf, name='export_pdf'),
]


