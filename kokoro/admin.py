from django.contrib import admin
from .models import Patient_profile

class Patient_profileAdmin(admin.ModelAdmin):
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")


admin.site.register(Patient_profile, Patient_profileAdmin)