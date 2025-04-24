from django.contrib import admin
from .models import Patient_profile, Clinical_Status, Clinical_evaluation, Comorbidities


class ClinicalEvaluationAdmin(admin.ModelAdmin):
    list_display = ['date_of_visit', 'EvaluationPreATC', 'symptoms', 'SVT', 'atrial_fibrillation', 'flutter',
                    'atrial_tachycardia', 'paroxysmal_supraventricular_tachycardia', 'wolff_parkinson_white', 
                    'besv', 'bev', 'premature_ventricular_contraction', 'thrombosis']
class ClinicalEvaluationInline(admin.TabularInline):
    model = Clinical_evaluation
    extra = 1

class ComorbiditiesAdmin(admin.ModelAdmin):
    list_display = ['arterial_hypertension']
class ComorbiditiesInline(admin.TabularInline):
    model = Clinical_evaluation
    extra = 1


class Patient_profileAdmin(admin.ModelAdmin):
     inlines = [
		ClinicalEvaluationInline,
		ComorbiditiesInline,
	]
     # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
     list_display = ("last_name", "first_name", "sex", "date_of_birth")


admin.site.register(Patient_profile, Patient_profileAdmin)
admin.site.register(Clinical_evaluation)
admin.site.register(Comorbidities)

