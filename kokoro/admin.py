from django.contrib import admin
from .models import Patient_profile, Clinical_Status, Clinical_evaluation

class Patient_profileAdmin(admin.ModelAdmin):
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")
	
admin.site.register(Patient_profile, Patient_profileAdmin)

class ClinicalEvaluationInline(admin.TabularInline):
    model = Clinical_evaluation
    extra = 1

admin.site.register(Clinical_Status)
class ClinicalStatusAdmin(admin.ModelAdmin):
    inlines = [ClinicalEvaluationInline]

admin.site.register(Clinical_evaluation)
class ClinicalEvaluationAdmin(admin.ModelAdmin):
    list_display = ['date_of_visit', 'EvaluationPreATC', 'symptoms', 'SVT', 'atrial_fibrillation']

