from django.contrib import admin
from .models import Patient_profile, Clinical_Status

class Patient_profileAdmin(admin.ModelAdmin):
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")
	
class Clinical_statusAdmin(admin.ModelAdmin):
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("date_of_visit", "symptoms")


admin.site.register(Patient_profile, Patient_profileAdmin)
admin.site.register(Clinical_Status, Clinical_statusAdmin)