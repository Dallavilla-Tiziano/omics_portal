from django.contrib import admin
from .models import (PatientProfile, Sample, DeviceType, DeviceInstance,
						DeviceEvent, Ablation, DeviceImplant, Clinical_Status,
						Clinical_evaluation, Symptoms, Comorbidities, EP_study,
						Flecainide_test, Adrenaline_test, Ajmaline_test, ECG,
						ECHO, Late_potentials, RMN_TC_PH, Therapy, ValveIntervention,
						CoronaryIntervention, ResearchAnalysis, PatientStudy,
						Study, Riskfactors, Cardiomiopathies, ClinicalEvent, Genetic_profile,
						Genetic_status, Genetic_test, Gene, Mutation, Doctors #Events
					)

class StudyAdmin(admin.ModelAdmin):
	list_display  = ['id','project_code','project_id','start_date','end_date']
	search_fields = ['project_code', 'project_id']

class PatientStudyInline(admin.TabularInline):
	model = PatientStudy
	extra = 0
	autocomplete_fields = ['study']
	fields = ['study', 'enrollment_date']

class ClinicalEvaluationAdmin(admin.ModelAdmin):
	autocomplete_fields = ['symptoms', 'cardiomiopathies', 'riskfactors', 'comorbidities']
	
	list_display = ['patient','date_of_visit']
class ClinicalEvaluationInline(admin.TabularInline):
	model = Clinical_evaluation
	extra = 0

class SymptomsAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']

class CardiomiopathiesAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']

class RiskfactorsAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']

class ComorbiditiesAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']

# class EventsAdmin(admin.ModelAdmin):
#     list_display = ['death']
# class EventsInline(admin.TabularInline):
#     model = Events
#     extra = 1

class ClinicalEventAdmin(admin.ModelAdmin):
	list_display = ("patient", "date", "clinical_event")

class AblationAdmin(admin.ModelAdmin):
	list_display = ("date", "total_area", "total_rf_time")
class AblationtInline(admin.TabularInline):
	model = Ablation
	extra = 0

class DeviceImplantAdmin(admin.ModelAdmin):
	list_display = ("date", "lv4_ring", "lv3_ring", "lv2_ring", "lv1_tip")
class DeviceImplantInline(admin.TabularInline):
	model = DeviceImplant
	extra = 0

class DeviceEventAdmin(admin.ModelAdmin):
	list_display = ("timestamp", "date", "inappropriate_pre_rf_shock_cause", "inappropriate_post_brs_shock_cause")
class DeviceEventInline(admin.TabularInline):
	model = DeviceEvent
	extra = 0



class DeviceTypeAdmin(admin.ModelAdmin):
	list_display = ("Model", "Design", "Company")

class DeviceInstanceAdmin(admin.ModelAdmin):

	list_display = ("device_type", "serial_number", "implant_date")

	def implant_date(self, obj):
		# for OneToOne: obj.implant
		# for FK: maybe obj.implants.latest('date')
		implant = getattr(obj, 'implant', None)
		return implant.date if implant else "-"
	implant_date.short_description = "Implant date"
	
	inlines = [
		DeviceEventInline,
	]
	
class DeviceInstanceInline(admin.TabularInline):
	model = DeviceInstance
	extra = 0



class SampleAdmin(admin.ModelAdmin):
	list_display = ("imtc_id", "patient", "procedure_type", "collection_date")
	search_fields = ['imtc_id']
class SampleInline(admin.TabularInline):
	model = Sample
	extra = 0
	def has_add_permission(self, request, obj=None):
		return False  # disables "Add another Patient study"



class EPStudyAdmin(admin.ModelAdmin):
	list_display = ("ep_result", "induced_arrhythmia")
class EPStudyInline(admin.TabularInline):
	model = EP_study
	extra = 0

class FlecainideTestAdmin(admin.ModelAdmin):
	list_display = ("flecainide_result", "flecainide_dose")
class FlecainideTestInline(admin.TabularInline):
	model = Flecainide_test
	extra = 0

class AdrenalineTestAdmin(admin.ModelAdmin):
	list_display = ("adrenaline_result", "adrenaline_dose")
class AdrenalineTestInline(admin.TabularInline):
	model = Adrenaline_test
	extra = 0

class AjmalineTestAdmin(admin.ModelAdmin):
	list_display = ("ajmaline_result", "ajmaline_dose")
class AjmalineTestInline(admin.TabularInline):
	model = Ajmaline_test
	extra = 0



class ECGAdmin(admin.ModelAdmin):
	list_display = ["atrial_rhythmh"]
class ECGInline(admin.TabularInline):
	model = ECG
	extra = 0

class ECHOAdmin(admin.ModelAdmin):
	list_display = ["anatomical_alterations"]
class ECHOInline(admin.TabularInline):
	model = ECHO
	extra = 0

class LatePotentialsAdmin(admin.ModelAdmin):
	list_display = ["basal_lp1"]
class LatePotentialsInline(admin.TabularInline):
	model = Late_potentials
	extra = 0

class RMTCPHAdmin(admin.ModelAdmin):
	list_display = ["anatomical_alterations"]
class RMTCPHInline(admin.TabularInline):
	model = RMN_TC_PH
	extra = 0



class TherapyAdmin(admin.ModelAdmin):
	search_fields = ['name']

class ResearchAnalysisAdmin(admin.ModelAdmin):
	autocomplete_fields = ['samples']
	list_display = ("analysis_name", "type")

class ValveInterventionAdmin(admin.ModelAdmin):
	list_display = ("replacement", "repair")
class ValveInterventionInLine(admin.TabularInline):	
	model = ValveIntervention
	extra = 0

class CoronaryInterventionAdmin(admin.ModelAdmin):
	list_display = ("cabg", "pci")
class CoronaryInterventionInLine(admin.TabularInline):	
	model = CoronaryIntervention
	extra = 0

class GeneticProfileAdmin(admin.ModelAdmin):
	list_display = ["FIN_number"]
class GeneticProfileInLine(admin.TabularInline):	
	model = Genetic_profile
	extra = 0

class GeneticStatusAdmin(admin.ModelAdmin):
	list_display = ["Patient_status"]
class GeneticStatusInLine(admin.TabularInline):	
	model = Genetic_status
	extra = 0

class GeneticTestAdmin(admin.ModelAdmin):
	autocomplete_fields = ('genes', 'var_p', 'var_c', 'editing_doctor', 'reporting_doctor') 
	list_display = ["Consent_date"]
class GeneticTestInLine(admin.TabularInline):	
	model = Genetic_test
	extra = 0

class GeneAdmin(admin.ModelAdmin):
	search_fields = ['name']

class MutationAdmin(admin.ModelAdmin):
	search_fields = ['name']

class DoctorsAdmin(admin.ModelAdmin):
	search_fields = ['name']

#class AminoacidchangeAdmin(admin.ModelAdmin):
#	search_fields = ['name']



class PatientProfileAdmin(admin.ModelAdmin):

	def formatted_date_of_birth(self, obj):
		return obj.date_of_birth.strftime('%d-%m-%Y')

	inlines = [
		SampleInline,
		AblationtInline,
		DeviceInstanceInline,
		DeviceImplantInline,
		# ClinicalEvaluationInline,
		# EventsInline,
		# EPStudyInline,
		# FlecainideTestInline,
		# ECGInline,
		# ECHOInline,
		LatePotentialsInline,
		# RMTCPHInline,
		ValveInterventionInLine,
		CoronaryInterventionInLine,
		PatientStudyInline,
		GeneticProfileInLine,
		GeneticStatusInLine,
		# GeneticTestInLine
	]
	# "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	autocomplete_fields = ['therapies','allergies','studies']
	list_display = ("last_name", "first_name", "sex", "formatted_date_of_birth")
	search_fields = ['last_name', 'first_name']

class PatientStudyAdmin(admin.ModelAdmin):
	list_display       = ['patient', 'study', 'enrollment_date']
	search_fields      = ['patient__last_name', 'study__project_id']
	autocomplete_fields = ['patient', 'study']

admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(DeviceInstance, DeviceInstanceAdmin)
admin.site.register(DeviceEvent, DeviceEventAdmin)
admin.site.register(Ablation, AblationAdmin)
admin.site.register(DeviceImplant, DeviceImplantAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Clinical_evaluation, ClinicalEvaluationAdmin)
admin.site.register(Symptoms, SymptomsAdmin)
admin.site.register(Cardiomiopathies, CardiomiopathiesAdmin)
admin.site.register(Riskfactors, RiskfactorsAdmin)
admin.site.register(Comorbidities, ComorbiditiesAdmin)
# admin.site.register(Events, EventsAdmin)
admin.site.register(EP_study, EPStudyAdmin)
admin.site.register(Flecainide_test, FlecainideTestAdmin)
admin.site.register(Adrenaline_test, AdrenalineTestAdmin)
admin.site.register(Ajmaline_test, AjmalineTestAdmin)
admin.site.register(ECG, ECGAdmin)
admin.site.register(ECHO, ECHOAdmin)
admin.site.register(Late_potentials, LatePotentialsAdmin)
admin.site.register(RMN_TC_PH, RMTCPHAdmin)
admin.site.register(Therapy, TherapyAdmin)
admin.site.register(ResearchAnalysis, ResearchAnalysisAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Genetic_profile, GeneticProfileAdmin)
admin.site.register(Genetic_status, GeneticStatusAdmin)
admin.site.register(Genetic_test, GeneticTestAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Mutation, MutationAdmin)
admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(ClinicalEvent, ClinicalEventAdmin)