from django import forms
from .models import Patient
from datetime import date


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "civility", "first_name", "last_name", "gender", "birth_date",
            "phone", "email", "address",
            "weight", "height", "is_pregnant",
            "allergies", "medications", "medical_history", "family_history", "lifestyle_notes",
            "consent",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "allergies": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "medical_history": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "family_history": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "lifestyle_notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    # ✅ VALIDATIONS PERSONNALISÉES
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date and birth_date > date.today():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")
        return birth_date

    def clean(self):
        cleaned_data = super().clean()

        # Si le genre est "Femme" et "is_pregnant" = True → OK
        # Si autre genre → empêche grossesse
        gender = cleaned_data.get("gender")
        is_pregnant = cleaned_data.get("is_pregnant")
        if is_pregnant and gender != "F":
            self.add_error("is_pregnant", "Ce champ ne peut être coché que pour une femme.")

        # Poids et taille logiques
        weight = cleaned_data.get("weight")
        height = cleaned_data.get("height")
        if weight and height:
            if not (20 <= weight <= 300):
                self.add_error("weight", "Le poids semble invalide.")
            if not (100 <= height <= 250):
                self.add_error("height", "La taille semble invalide.")

        # Consentement obligatoire
        consent = cleaned_data.get("consent")
        if not consent:
            self.add_error("consent", "Vous devez accepter le consentement avant de soumettre.")

        return cleaned_data
