from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Patient(models.Model):
    CIVILITY_CHOICES = [
        ('M', 'Monsieur'),
        ('F', 'Madame'),
        ('A', 'Autre'),
    ]

    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]

    civility = models.CharField("Civilité", max_length=1, choices=CIVILITY_CHOICES, default='M')
    first_name = models.CharField("Prénom", max_length=150)
    last_name = models.CharField("Nom", max_length=150)
    gender = models.CharField("Sexe", max_length=1, choices=GENDER_CHOICES, default='A')
    birth_date = models.DateField("Date de naissance", null=True, blank=True)

    phone = models.CharField("Téléphone", max_length=30, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.TextField("Adresse", blank=True, null=True)

    weight = models.DecimalField("Poids (kg)", max_digits=5, decimal_places=2,
                                 null=True, blank=True,
                                 validators=[MinValueValidator(20), MaxValueValidator(300)])
    height = models.DecimalField("Taille (cm)", max_digits=5, decimal_places=2,
                                 null=True, blank=True,
                                 validators=[MinValueValidator(100), MaxValueValidator(250)])

    is_pregnant = models.BooleanField("Grossesse en cours ?", default=False)
    allergies = models.TextField("Allergies connues", blank=True, null=True)
    medications = models.TextField("Médicaments actuels", blank=True, null=True)
    medical_history = models.TextField("Antécédents médicaux", blank=True, null=True)
    family_history = models.TextField("Antécédents familiaux", blank=True, null=True)
    lifestyle_notes = models.TextField("Habitudes de vie (alimentation, sommeil, sport…)",
                                       blank=True, null=True)

    consent = models.BooleanField(
        "J’accepte que mes données soient utilisées à des fins de suivi médical",
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email or self.phone})"

    @property
    def bmi(self):
        """Calcul IMC (Indice de Masse Corporelle) si poids et taille fournis"""
        if self.weight and self.height:
            return round(float(self.weight) / ((float(self.height) / 100) ** 2), 2)
        return None



