import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from .forms import PatientForm
from .models import Patient
from django.contrib import messages

def questionnaire_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            print("✅ Formulaire valide, redirection vers thanks...")
            form.save()
            messages.success(request, "Questionnaire enregistré, merci.")
            return redirect(reverse("questionnaire:thanks"))
        else:
            print("❌ Formulaire invalide :", form.errors)
    else:
        form = PatientForm()

    return render(request, "questionnaire/form.html", {"form": form})


def thanks(request):
    # délai configurable (en secondes)
    context = {'redirect_delay': 10}  # par ex. 10 secondes
    return render(request, "questionnaire/thanks.html", context)


def patient_list(request):
    patients = Patient.objects.order_by("-created_at")
    return render(request, "questionnaire/list.html", {"patients": patients})

def export_patients_csv(request):
    # Créer la réponse HTTP avec type CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'

    writer = csv.writer(response)
    # Écrire l'entête
    writer.writerow([
        'Civility', 'First Name', 'Last Name', 'Gender', 'Birth Date',
        'Phone', 'Email', 'Address', 'Weight', 'Height', 'Is Pregnant',
        'Allergies', 'Medications', 'Medical History', 'Family History',
        'Lifestyle Notes', 'Consent', 'Created At'
    ])

    # Écrire les données
    for patient in Patient.objects.all().order_by('-created_at'):
        writer.writerow([
            patient.civility, patient.first_name, patient.last_name,
            patient.gender, patient.birth_date, patient.phone, patient.email,
            patient.address, patient.weight, patient.height, patient.is_pregnant,
            patient.allergies, patient.medications, patient.medical_history,
            patient.family_history, patient.lifestyle_notes, patient.consent,
            patient.created_at
        ])

    return response

def export_patients_pdf(request):
    patients = Patient.objects.all().order_by('-created_at')
    template = get_template('questionnaire/patients_pdf.html')
    html = template.render({'patients': patients})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="patients.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF')

    return response



