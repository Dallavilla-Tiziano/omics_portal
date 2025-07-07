from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django import forms
from kokoro.models import (
	PatientProfile, Late_potentials, Study,
	Ablation, Adrenaline_test, Ajmaline_test,
	Clinical_evaluation, ClinicalEvent, CoronaryIntervention,
	DeviceEvent, DeviceImplant, DeviceInstance,
	EP_study, ECG, ECHO,
	Flecainide_test, Genetic_profile, Genetic_status,
	Genetic_test, RMN_TC_PH, Sample, ResearchAnalysis,
	ValveIntervention,
)
from kokoro.forms import (
	PatientProfileForm, LatePotentialForm, StudyForm,
	AblationForm, AdrenalineTestForm, AjmalineTestForm,
	Clinical_evaluationForm, ClinicalEventForm, CoronaryInterventionForm,
	DeviceEventForm, DeviceImplantForm, DeviceInstanceForm,
	EP_studyForm, ECGForm, ECHOForm,
	Flecainide_testForm, Genetic_profileForm, Genetic_statusForm,
	Genetic_testForm, RMN_TC_PHTest, SampleForm, ResearchAnalysisForm,
	ValveInterventionForm,
)

# Parent search configuration
PARENT_CONFIG = {
	'patientprofile': {
		'model': PatientProfile,
		'search_fields': ['last_name__icontains', 'first_name__icontains', 'cardioref_id__icontains'],
	},
	'deviceinstance': {
		'model': DeviceInstance,
		'search_fields': ['serial_number__icontains'],
	},
	'sample': {
		'model': Sample,
		'search_fields': ['imtc_id__icontains'],
	},
	'study': {
		'model': Study,
		'search_fields': ['project_id__icontains', 'project_code__icontains'],
	},
}

# Mapping of parent to child types
PARENT_CHILD_MAP = {
	'patientprofile': [
		('ablation', 'Ablation', 'add_ablation'),
		('adrenaline_test', 'Adrenaline Test', 'add_adrenaline_test'),
		('ajmaline_test', 'Ajmaline Test', 'add_ajmaline_test'),
		('clinicalevent', 'Clinical Event', 'add_clinicalevent'),
		('clinical_evaluation', 'Clinical Evaluation', 'add_clinical_evaluation'),
		('coronaryintervention', 'Coronary Intervention', 'add_coronaryintervention'),
		('deviceinstance', 'Device Instance', 'add_deviceinstance'),
		('deviceimplant', 'Device Implant', 'add_deviceimplant'),
		('deviceevent', 'Device Event', 'add_deviceevent'),
		('ecg', 'ECG', 'add_ecg'),
		('echo', 'ECHO', 'add_echo'),
		('ep_study', 'EP Study', 'add_ep_study'),
		('flecainide_test', 'Flecainide Test', 'add_flecainide_test'),
		('latepotential', 'Late Potentials', 'add_latepotential'),
		('genetic_profile', 'Genetic Profile', 'add_genetic_profile'),
		('genetic_status', 'Genetic Status', 'add_genetic_status'),
		('genetic_test', 'Genetic Test', 'add_genetic_test'),
		('sample', 'Sample', 'add_sample'),
		('valveintervention', 'Valve Intervention', 'add_valveintervention'),
	],
	'deviceinstance': [
		('deviceevent', 'Device Event', 'add_deviceevent'),
		('deviceimplant', 'Device Implant', 'add_deviceimplant'),
	],
	'sample': [
		('researchanalysis', 'Research Analysis', 'add_researchanalysis'),
	],
	'study': [
		('studyenrollment', 'Patient Study Enrollment', 'add_patientstudy'),
	],
}

class ParentAttachMixin:
	"""
	Mixin to attach a parent to a new child instance.
	Requires each CreateView to define `parent_field`.
	"""
	parent_field: str

	def dispatch(self, request, *args, **kwargs):
		cfg = PARENT_CONFIG[kwargs['parent_type']]
		self.parent_obj = get_object_or_404(cfg['model'], pk=kwargs['parent_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		setattr(form.instance, self.parent_field, self.parent_obj)
		return super().form_valid(form)

class ChildTypeListView(TemplateView):
	template_name = 'submissions/parent_children.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		parent_type = kwargs['parent_type']
		parent_id = kwargs['parent_id']
		parent_obj = get_object_or_404(PARENT_CONFIG[parent_type]['model'], pk=parent_id)
		children = []
		for key, label, url_name in PARENT_CHILD_MAP[parent_type]:
			url = reverse(f'submissions:{url_name}', args=[parent_type, parent_id])
			children.append({'label': label, 'url': url})
		context.update({'parent_obj': parent_obj, 'children': children})
		return context

class ParentAttachMixin:
    parent_field: str

    def dispatch(self, request, *args, **kwargs):
        cfg = PARENT_CONFIG[kwargs['parent_type']]
        self.parent_obj = get_object_or_404(cfg['model'], pk=kwargs['parent_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # set initial & hide the parent dropdown
        if self.parent_field in form.fields:
            form.fields[self.parent_field].initial = self.parent_obj.pk
            form.fields[self.parent_field].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        setattr(form.instance, self.parent_field, self.parent_obj)
        return super().form_valid(form)

class ParentSearchView(TemplateView):
	template_name = 'submissions/parent_search.html'

	def get_context_data(self, **kwargs):
		from django.db.models import Q
		context = super().get_context_data(**kwargs)
		parent_type = self.request.GET.get('parent_type')
		q = self.request.GET.get('q')
		results = []
		if parent_type and q:
			cfg = PARENT_CONFIG.get(parent_type)
			qs = cfg['model'].objects.all()
			# Combine filters with OR across search_fields
			query = Q()
			for field in cfg['search_fields']:
				query |= Q(**{field: q})
			results = qs.filter(query)
		context.update({'results': results, 'parent_type': parent_type})
		return context

class ChildTypeListView(TemplateView):
	template_name = 'submissions/parent_children.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		parent_type = kwargs['parent_type']; parent_id = kwargs['parent_id']
		parent_obj = get_object_or_404(PARENT_CONFIG[parent_type]['model'], pk=parent_id)
		children = []
		for key, label, url_name in PARENT_CHILD_MAP[parent_type]:
			url = reverse(f'submissions:{url_name}', args=[parent_type, parent_id])
			children.append({'label': label, 'url': url})
		context.update({'parent_obj': parent_obj, 'children': children})
		return context

# -------------------- CREATE VIEWS --------------------
for cls in [
	(Ablation, AblationForm, 'ablation_form.html', 'patient'),
	(Adrenaline_test, AdrenalineTestForm, 'adrenaline_test_form.html', 'patient'),
	(Ajmaline_test, AjmalineTestForm, 'ajmaline_test_form.html', 'patient'),
	(ClinicalEvent, ClinicalEventForm, 'clinicalevent_form.html', 'patient'),
	(Clinical_evaluation, Clinical_evaluationForm, 'clinical_evaluation_form.html', 'patient'),
	(CoronaryIntervention, CoronaryInterventionForm, 'coronaryintervention_form.html', 'patient'),
	(DeviceInstance, DeviceInstanceForm, 'deviceinstance_form.html', 'patient'),
	(DeviceImplant, DeviceImplantForm, 'deviceimplant_form.html', 'patient'),
	(DeviceEvent, DeviceEventForm, 'deviceevent_form.html', 'device'),
	(ECG, ECGForm, 'ecg_form.html', 'patient'),
	(ECHO, ECHOForm, 'echo_form.html', 'patient'),
	(EP_study, EP_studyForm, 'ep_study_form.html', 'patient'),
	(Flecainide_test, Flecainide_testForm, 'flecainide_test_form.html', 'patient'),
	(Late_potentials, LatePotentialForm, 'latepotential_form.html', 'patient'),
	(Genetic_profile, Genetic_profileForm, 'genetic_profile_form.html', 'patient'),
	(Genetic_status, Genetic_statusForm, 'genetic_status_form.html', 'patient'),
	(Genetic_test, Genetic_testForm, 'genetic_test_form.html', 'patient'),
	(RMN_TC_PH, RMN_TC_PHTest, 'rmn_tc_phtest_form.html', 'patient'),
	(Sample, SampleForm, 'sample_form.html', 'patient'),
	(ValveIntervention, ValveInterventionForm, 'valveintervention_form.html', 'patient'),
	(ResearchAnalysis, ResearchAnalysisForm, 'researchanalysis_form.html', 'samples'),
]:
	name = f"{cls[0].__name__}CreateView"
	globals()[name] = type(
		name,
		(LoginRequiredMixin, ParentAttachMixin, CreateView),
		{
			'model': cls[0],
			'form_class': cls[1],
			'parent_field': cls[3],
			'template_name': f"submissions/{cls[2]}",
			'success_url': reverse_lazy('submissions:submission_success'),
		}
	)

# -------------------- UPDATE VIEWS --------------------
for cls in [
	(Ablation, AblationForm, 'ablation_form.html'),
	(Adrenaline_test, AdrenalineTestForm, 'adrenaline_test_form.html'),
	(Ajmaline_test, AjmalineTestForm, 'ajmaline_test_form.html'),
	(ClinicalEvent, ClinicalEventForm, 'clinicalevent_form.html'),
	(Clinical_evaluation, Clinical_evaluationForm, 'clinical_evaluation_form.html'),
	(CoronaryIntervention, CoronaryInterventionForm, 'coronaryintervention_form.html'),
	(DeviceInstance, DeviceInstanceForm, 'deviceinstance_form.html'),
	(DeviceImplant, DeviceImplantForm, 'deviceimplant_form.html'),
	(DeviceEvent, DeviceEventForm, 'deviceevent_form.html'),
	(ECG, ECGForm, 'ecg_form.html'),
	(ECHO, ECHOForm, 'echo_form.html'),
	(EP_study, EP_studyForm, 'ep_study_form.html'),
	(Flecainide_test, Flecainide_testForm, 'flecainide_test_form.html'),
	(Late_potentials, LatePotentialForm, 'latepotential_form.html'),
	(Genetic_profile, Genetic_profileForm, 'genetic_profile_form.html'),
	(Genetic_status, Genetic_statusForm, 'genetic_status_form.html'),
	(Genetic_test, Genetic_testForm, 'genetic_test_form.html'),
	(RMN_TC_PH, RMN_TC_PHTest, 'rmn_tc_phtest_form.html'),
	(Sample, SampleForm, 'sample_form.html'),
	(ValveIntervention, ValveInterventionForm, 'valveintervention_form.html'),
	(PatientProfile, PatientProfileForm, 'patientprofile_form.html'),
]:
	name = f"{cls[0].__name__}UpdateView"
	globals()[name] = type(
		name,
		(LoginRequiredMixin, UpdateView),
		{
			'model': cls[0],
			'form_class': cls[1],
			'template_name': f"submissions/{cls[2]}",
			'success_url': reverse_lazy('submissions:submission_success'),
		}
	)

	# Standalone CreateView for PatientProfile (missing in dynamic loop)
class PatientProfileCreateView(LoginRequiredMixin, CreateView):
	model = PatientProfile
	form_class = PatientProfileForm
	template_name = 'submissions/patientprofile_form.html'
	success_url = reverse_lazy('submissions:submission_success')

# Alias for Late_potentials views to match expected class names in urls.py
LatePotentialCreateView = Late_potentialsCreateView
LatePotentialUpdateView = Late_potentialsUpdateView

# Standalone Create/Update for Study model (missing)
class StudyCreateView(LoginRequiredMixin, CreateView):
	model = Study
	form_class = StudyForm
	template_name = 'submissions/study_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class StudyUpdateView(LoginRequiredMixin, UpdateView):
	model = Study
	form_class = StudyForm
	template_name = 'submissions/study_form.html'
	success_url = reverse_lazy('submissions:submission_success')