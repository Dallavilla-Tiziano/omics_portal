from django.contrib import admin
from .models import Patient_profile, Sample

class Patient_profileAdmin(admin.ModelAdmin):
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")

class SampleAdmin(admin.ModelAdmin):
    list_display = ("imtc_id", "patient", "procedure_type", "collection_date")

admin.site.register(Patient_profile, Patient_profileAdmin)
admin.site.register(Sample, SampleAdmin)