from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "phone", "bmi", "created_at")
    list_filter = ("gender", "is_pregnant", "created_at")
    search_fields = ("last_name", "first_name", "email", "phone")
    readonly_fields = ("bmi", "created_at", "updated_at")
