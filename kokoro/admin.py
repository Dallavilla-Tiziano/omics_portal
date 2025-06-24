from .forms import (PatientProfileForm, LatePotentialForm, StudyForm, AblationForm)
from django.contrib import admin
from django.utils.html import format_html_join, mark_safe
from tabbed_admin import TabbedModelAdmin
from .models import (PatientProfile, Sample, DeviceType, DeviceInstance,
						DeviceEvent, Ablation, DeviceImplant, Clinical_Status,
						Clinical_evaluation, Symptoms, Comorbidities, EP_study,
						Flecainide_test, Adrenaline_test, Ajmaline_test, ECG,
						ECHO, Late_potentials, RMN_TC_PH, Therapy, ValveIntervention,
						CoronaryIntervention, ResearchAnalysis, PatientStudy,
						Study, Riskfactors, Cardiomiopathies, ClinicalEvent, Genetic_profile,
						Genetic_status, Genetic_test, Gene, Mutation, Doctors #Events
					)

class AblationAdmin(admin.ModelAdmin):
	form = AblationForm
	list_display = ('patient', 'date')
	search_fields = ['patient__first_name', 'patient__last_name']
class AblationtInline(admin.TabularInline):
	form = AblationForm
	model = Ablation
	extra = 0

class StudyAdmin(admin.ModelAdmin):
	form = StudyForm
	list_display  = ['project_code','project_id','start_date','end_date']
	search_fields = ['project_code', 'project_id']

class PatientStudyInline(admin.TabularInline):
	form = StudyForm
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

class ClinicalEventAdmin(admin.ModelAdmin):
	list_display = ("patient", "date", "clinical_event")



class DeviceImplantAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name','patient__last_name','date')
	search_fields = ['patient__first_name', 'patient__last_name']
class DeviceImplantInline(admin.TabularInline):
	model = DeviceImplant
	extra = 0

class DeviceEventAdmin(admin.ModelAdmin):
	list_display = ('device__serial_number', 'timestamp', 'date', 'inappropriate_pre_rf_shock_cause', 'inappropriate_post_brs_shock_cause')
	search_fields = ['device__serial_number']
class DeviceEventInline(admin.TabularInline):
	model = DeviceEvent
	extra = 0

class DeviceTypeAdmin(admin.ModelAdmin):
		list_display = ("model", "design", "company")

class DeviceInstanceAdmin(admin.ModelAdmin):

	list_display = ('device_type', 'serial_number', 'implant_date')
	search_fields = ['serial_number', 'patient__first_name', 'patient__first_name']
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
	list_display = ('imtc_id', 'patient', 'procedure_type', 'collection_date')
	search_fields = ['patient__first_name', 'patient__last_name', 'imtc_id']
class SampleInline(admin.StackedInline):
	model = Sample
	extra = 0


class EPStudyAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_provocative_test', 'ep_result')
	search_fields = ['patient__first_name', 'patient__last_name']
class EPStudyInline(admin.TabularInline):
	model = EP_study
	extra = 0

class FlecainideTestAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_provocative_test', 'flecainide_result')
	search_fields = ['patient__first_name', 'patient__last_name']
class FlecainideTestInline(admin.TabularInline):
	model = Flecainide_test
	extra = 0

class AdrenalineTestAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_provocative_test', 'adrenaline_result')
	search_fields = ['patient__first_name', 'patient__last_name']
class AdrenalineTestInline(admin.TabularInline):
	model = Adrenaline_test
	extra = 0

class AjmalineTestAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_provocative_test', 'ajmaline_result')
	search_fields = ['patient__first_name', 'patient__last_name']
class AjmalineTestInline(admin.TabularInline):
	model = Ajmaline_test
	extra = 0



class ECGAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_exam')
	search_fields = ['patient__first_name', 'patient__last_name']
class ECGInline(admin.TabularInline):
	model = ECG
	extra = 0

class ECHOAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_exam')
	search_fields = ['patient__first_name', 'patient__last_name']
class ECHOInline(admin.StackedInline):
	model = ECHO
	extra = 0

class LatePotentialsAdmin(admin.ModelAdmin):
	form = LatePotentialForm
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_exam')
	search_fields = ['patient__first_name', 'patient__last_name']
class LatePotentialsInline(admin.TabularInline):
	form = LatePotentialForm
	model = Late_potentials
	extra = 0

class RMTCPHAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'date_of_exam')
	search_fields = ['patient__first_name', 'patient__last_name']
class RMTCPHInline(admin.TabularInline):
	model = RMN_TC_PH
	extra = 0



class TherapyAdmin(admin.ModelAdmin):
	search_fields = ['name']

class ResearchAnalysisAdmin(admin.ModelAdmin):
	search_fields = ['analysis_name']
	autocomplete_fields = ['samples']
	list_display = ('analysis_name', 'type', 'date_performed')

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
	list_display = ('patient__first_name', 'patient__last_name', 'FIN_number', 'PIN_number', 'FIN_progressive_genetics')
	search_fields = ['patient__first_name', 'patient__last_name']
class GeneticProfileInLine(admin.TabularInline):	
	model = Genetic_profile
	extra = 0

class GeneticStatusAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'patient_status')
	search_fields = ['patient__first_name', 'patient__last_name']
class GeneticStatusInLine(admin.TabularInline):	
	model = Genetic_status
	extra = 0

class GeneticTestAdmin(admin.ModelAdmin):
	list_display = ('patient__first_name', 'patient__last_name', 'report_data')
	search_fields = ['patient__first_name', 'patient__last_name']
	autocomplete_fields = ('genes', 'var_p', 'var_c', 'editing_doctor', 'reporting_doctor') 
class GeneticTestInLine(admin.StackedInline):
	autocomplete_fields = ('genes', 'var_p', 'var_c', 'editing_doctor', 'reporting_doctor')
	model = Genetic_test
	extra = 0

class GeneAdmin(admin.ModelAdmin):
	search_fields = ['name']

class MutationAdmin(admin.ModelAdmin):
	search_fields = ['name']

class DoctorsAdmin(admin.ModelAdmin):
	search_fields = ['name']

class PatientProfileAdmin(TabbedModelAdmin):
	
	form = PatientProfileForm
	
	def formatted_date_of_birth(self, obj):
		return obj.date_of_birth.strftime('%d-%m-%Y')

	autocomplete_fields = ['therapies', 'allergies', 'studies']
	list_display = ("last_name", "first_name", "sex", "formatted_date_of_birth")
	# list_display = ("id", "sex", "formatted_date_of_birth")
	readonly_fields = ['related_analyses_display']
	search_fields = ['last_name', 'first_name']

	def related_analyses_display(self, obj):
		# Get all ResearchAnalysis objects that include any sample from this patient
		analyses = ResearchAnalysis.objects.filter(samples__patient=obj).distinct()

		if not analyses.exists():
			return "No related analyses."

		return format_html_join(
			mark_safe('<br>'),
			'<strong>{}</strong>: {}',
			((a.get_type_display(), a.date_performed) for a in analyses)
		)

	related_analyses_display.short_description = "Related Omics Analyses"

	tab_patient = (
		(None, {
			'fields': ('last_name', 'first_name', 'date_of_birth',
			 'nation', 'region', 'province', 'height', 'weight', 'cardioref_id', 'therapies', 'allergies', 'studies','related_analyses_display')
		}),
	)

	tab_sample = (
		SampleInline,
		)
	tab_abl = (
		AblationtInline,
		)
	tab_dev_ins = (
		DeviceInstanceInline,
		)
	tab_dev_imp = (
		DeviceImplantInline,
		)
	tab_clin_eva = (
		ClinicalEvaluationInline,
		)
	tab_eps = (
		EPStudyInline,
		)
	tab_fleca = (
		FlecainideTestInline,
		)
	tab_ecg = (
		ECGInline,
		)
	tab_echo = (
		ECHOInline,
		)
	tab_lpot = (
		LatePotentialsInline,
		)
	tab_rmt = (
		RMTCPHInline,
		)
	tab_valve = (
		ValveInterventionInLine,
		)
	tab_coro = (
		CoronaryInterventionInLine,
		)
	tab_pat_study = (
		PatientStudyInline,
		)
	tab_gen_p = (
		GeneticProfileInLine,
		)
	tab_gen_s = (
		GeneticStatusInLine,
		)
	tab_gen_t = (
		GeneticTestInLine,
		)

	tabs = [
	('Patient', tab_patient),
	('Samples', tab_sample),
	('Ablations', tab_abl),
	('Devices', tab_dev_ins),
	('Implants', tab_dev_imp),
	('Clinical Evaluations', tab_clin_eva),
	('EPS', tab_eps),
	('Flecanide Tests', tab_fleca),
	('ECG', tab_ecg),
	('Echographies', tab_echo),
	('Late Potentials', tab_lpot),
	('RMT', tab_rmt),
	('Valve interventions', tab_valve),
	('Coronary interventions', tab_coro),
	('Studies', tab_pat_study),
	('Genetic Profiles', tab_gen_p),
	('Genetic Status', tab_gen_s),
	('Genetic tests', tab_gen_t)
	]

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
admin.site.register(ValveIntervention, ValveInterventionAdmin)
admin.site.register(CoronaryIntervention, CoronaryInterventionAdmin)