from django.contrib import admin
from .models import PatientProfile, Sample, DeviceType, DeviceInstance, DeviceEvent, Ablation, DeviceImplant, Clinical_Status, Clinical_evaluation, Symptoms, Comorbidities, EP_study, Flecainide_test, Adrenaline_test, Ajmaline_test, ECG, ECHO, Late_potentials, RMN_TC_PH, Therapy, ValveIntervention, CoronaryIntervention, ResearchAnalysis, PatientStudy, Study, Riskfactors, Cardiomiopathies, Genetic_profile, Genetic_status, Genetic_test


class StudyAdmin(admin.ModelAdmin):
    list_display  = ['name', 'start_date', 'end_date']
    search_fields = ['name']

class PatientStudyInline(admin.TabularInline):
    model = PatientStudy
    extra = 1
    autocomplete_fields = ['study']
    fields = ['study', 'enrollment_date']

class ClinicalEvaluationAdmin(admin.ModelAdmin):
	autocomplete_fields = ['symptoms', 'cardiomiopathies', 'riskfactors', 'comorbidities']
	
	list_display = ['date_of_visit']
class ClinicalEvaluationInline(admin.TabularInline):
    model = Clinical_evaluation
    extra = 1

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



class AblationAdmin(admin.ModelAdmin):
	list_display = ("date", "total_area", "total_rf_time")
class AblationtInline(admin.TabularInline):
	model = Ablation
	extra = 1

class DeviceImplantAdmin(admin.ModelAdmin):
		list_display = ("date", "lv4_ring", "lv3_ring", "lv2_ring", "lv1_tip")
class DeviceImplantInline(admin.TabularInline):
	model = DeviceImplant
	extra = 1

class DeviceEventAdmin(admin.ModelAdmin):
		list_display = ("timestamp", "date", "inappropriate_pre_rf_shock_cause", "inappropriate_post_brs_shock_cause")
class DeviceEventInline(admin.TabularInline):
	model = DeviceEvent
	extra = 1



class DeviceTypeAdmin(admin.ModelAdmin):
		list_display = ("Model", "Design", "Company")

class DeviceInstanceAdmin(admin.ModelAdmin):#
	inlines = [
		DeviceEventInline,
	]
	list_display = ("device_type", "serial_number", "implantation")
class DeviceInstanceInline(admin.TabularInline):
	model = DeviceInstance
	extra = 1



class SampleAdmin(admin.ModelAdmin):
	list_display = ("imtc_id", "patient", "procedure_type", "collection_date")
	search_fields = ['imtc_id']
class SampleInline(admin.TabularInline):
	model = Sample
	extra = 1



class EPStudyAdmin(admin.ModelAdmin):
	list_display = ("ep_result", "induced_arrhythmia")
class EPStudyInline(admin.TabularInline):
	model = EP_study
	extra = 1

class FlecainideTestAdmin(admin.ModelAdmin):
	list_display = ("flecainide_result", "flecainide_dose")
class FlecainideTestInline(admin.TabularInline):
	model = Flecainide_test
	extra = 1

class AdrenalineTestAdmin(admin.ModelAdmin):
	list_display = ("adrenaline_result", "adrenaline_dose")
class AdrenalineTestInline(admin.TabularInline):
	model = Adrenaline_test
	extra = 1

class AjmalineTestAdmin(admin.ModelAdmin):
	list_display = ("ajmaline_result", "ajmaline_dose")
class AjmalineTestInline(admin.TabularInline):
	model = Ajmaline_test
	extra = 1



class ECGAdmin(admin.ModelAdmin):
	list_display = ["atrial_rhythmh"]
class ECGInline(admin.TabularInline):
	model = ECG
	extra = 1

class ECHOAdmin(admin.ModelAdmin):
	list_display = ["anatomical_alterations"]
class ECHOInline(admin.TabularInline):
	model = ECHO
	extra = 1

class LatePotentialsAdmin(admin.ModelAdmin):
	list_display = ["basal_lp1"]
class LatePotentialsInline(admin.TabularInline):
	model = Late_potentials
	extra = 1

class RMTCPHAdmin(admin.ModelAdmin):
	list_display = ["anatomical_alterations"]
class RMTCPHInline(admin.TabularInline):
	model = RMN_TC_PH
	extra = 1



class TherapyAdmin(admin.ModelAdmin):
	search_fields = ['name']

class ResearchAnalysisAdmin(admin.ModelAdmin):
	autocomplete_fields = ['samples']
	list_display = ("analysis_name", "type")

class ValveInterventionAdmin(admin.ModelAdmin):
	list_display = ("replacement", "repair")
class ValveInterventionInLine(admin.TabularInline):	
    model = ValveIntervention
    extra = 1

class CoronaryInterventionAdmin(admin.ModelAdmin):
	list_display = ("cabg", "pci")
class CoronaryInterventionInLine(admin.TabularInline):	
    model = CoronaryIntervention
    extra = 1

class GeneticProfileAdmin(admin.ModelAdmin):
	list_display = ["FIN_number"]
class GeneticProfileInLine(admin.TabularInline):	
    model = Genetic_profile
    extra = 1

class GeneticStatusAdmin(admin.ModelAdmin):
	list_display = ["Patient_status"]
class GeneticStatusInLine(admin.TabularInline):	
    model = Genetic_status
    extra = 1

class GeneticTestAdmin(admin.ModelAdmin):
	list_display = ["Consent_date"]
class GeneticTestInLine(admin.TabularInline):	
    model = Genetic_test
    extra = 1



class PatientProfileAdmin(admin.ModelAdmin):
	inlines = [
		SampleInline,
		AblationtInline,
		DeviceInstanceInline,
		DeviceImplantInline,
		ClinicalEvaluationInline,
		# EventsInline,
		EPStudyInline,
		FlecainideTestInline,
		ECGInline,
		ECHOInline,
		LatePotentialsInline,
		RMTCPHInline,
		ValveInterventionInLine,
		CoronaryInterventionInLine,
		PatientStudyInline,
		GeneticProfileInLine,
		GeneticStatusInLine,
		GeneticTestInLine
	]
	# "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	autocomplete_fields = ['therapies','allergies']
	list_display = ("last_name", "first_name", "sex", "date_of_birth")
	search_fields = ['last_name', 'first_name']

class PatientStudyAdmin(admin.ModelAdmin):
    list_display       = ['patient', 'study', 'enrollment_date']
    search_fields      = ['patient__last_name', 'study__name']
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