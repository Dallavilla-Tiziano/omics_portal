from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from kokoro.models import (
						PatientProfile, Late_potentials, Study,
						Ablation, Adrenaline_test, Ajmaline_test,
						Clinical_evaluation, ClinicalEvent, CoronaryIntervention,
						DeviceEvent, DeviceImplant, DeviceInstance,
						EP_study, ECG, ECHO,
						Flecainide_test, Genetic_profile, Genetic_status,
						Genetic_test, RMN_TC_PH, Sample,
						ValveIntervention,
					)
from kokoro.forms import (
						PatientProfileForm, LatePotentialForm, StudyForm,
						AblationForm, AdrenalineTestForm, AjmalineTestForm,
						Clinical_evaluationForm, ClinicalEventForm, CoronaryInterventionForm,
						DeviceEventForm, DeviceImplantForm, DeviceInstanceForm,
						EP_studyForm, ECGForm, ECHOForm,
						Flecainide_testForm, Genetic_profileForm, Genetic_statusForm,
						Genetic_testForm, RMN_TC_PHTest, SampleForm,
						ValveInterventionForm,
					)


class ValveInterventionCreateView(LoginRequiredMixin, CreateView):
	model = ValveIntervention
	form_class = ValveInterventionForm
	template_name = 'submissions/valveintervention_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class ValveInterventionUpdateView(LoginRequiredMixin, UpdateView):
	model = ValveIntervention
	form_class = ValveInterventionForm
	template_name = 'submissions/valveintervention_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return ValveIntervention.objects.all()

class SampleCreateView(LoginRequiredMixin, CreateView):
	model = Sample
	form_class = SampleForm
	template_name = 'submissions/sample_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class SampleUpdateView(LoginRequiredMixin, UpdateView):
	model = Sample
	form_class = SampleForm
	template_name = 'submissions/sample_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Sample.objects.all()

class RMN_TC_PHCreateView(LoginRequiredMixin, CreateView):
	model = RMN_TC_PH
	form_class = RMN_TC_PHTest
	template_name = 'submissions/rmn_tc_phtest_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class RMN_TC_PHUpdateView(LoginRequiredMixin, UpdateView):
	model = RMN_TC_PH
	form_class = RMN_TC_PHTest
	template_name = 'submissions/rmn_tc_phtest_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return RMN_TC_PH.objects.all()

class Genetic_testCreateView(LoginRequiredMixin, CreateView):
	model = Genetic_test
	form_class = Genetic_testForm
	template_name = 'submissions/genetic_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Genetic_testUpdateView(LoginRequiredMixin, UpdateView):
	model = Genetic_test
	form_class = Genetic_testForm
	template_name = 'submissions/genetic_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Genetic_test.objects.all()

class Genetic_statusCreateView(LoginRequiredMixin, CreateView):
	model = Genetic_status
	form_class = Genetic_statusForm
	template_name = 'submissions/genetic_status_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Genetic_statusUpdateView(LoginRequiredMixin, UpdateView):
	model = Genetic_status
	form_class = Genetic_statusForm
	template_name = 'submissions/genetic_status_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Genetic_status.objects.all()

class Genetic_profileCreateView(LoginRequiredMixin, CreateView):
	model = Genetic_profile
	form_class = Genetic_profileForm
	template_name = 'submissions/genetic_profile_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Genetic_profileUpdateView(LoginRequiredMixin, UpdateView):
	model = Genetic_profile
	form_class = Genetic_profileForm
	template_name = 'submissions/genetic_profile_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Genetic_profile.objects.all()

class Flecainide_testCreateView(LoginRequiredMixin, CreateView):
	model = Flecainide_test
	form_class = Flecainide_testForm
	template_name = 'submissions/flecainide_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Flecainide_testUpdateView(LoginRequiredMixin, UpdateView):
	model = Flecainide_test
	form_class = Flecainide_testForm
	template_name = 'submissions/flecainide_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Flecainide_test.objects.all()

class ECHOCreateView(LoginRequiredMixin, CreateView):
	model = ECHO
	form_class = ECHOForm
	template_name = 'submissions/echo_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class ECHOUpdateView(LoginRequiredMixin, UpdateView):
	model = ECHO
	form_class = ECHOForm
	template_name = 'submissions/echo_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return ECHO.objects.all()

class ECGCreateView(LoginRequiredMixin, CreateView):
	model = ECG
	form_class = ECGForm
	template_name = 'submissions/ecg_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class ECGUpdateView(LoginRequiredMixin, UpdateView):
	model = ECG
	form_class = ECGForm
	template_name = 'submissions/ecg_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return ECG.objects.all()

class EP_studyCreateView(LoginRequiredMixin, CreateView):
	model = EP_study
	form_class = EP_studyForm
	template_name = 'submissions/ep_study_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class EP_studyUpdateView(LoginRequiredMixin, UpdateView):
	model = EP_study
	form_class = EP_studyForm
	template_name = 'submissions/ep_study_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return EP_studyForm.objects.all()

class DeviceInstanceCreateView(LoginRequiredMixin, CreateView):
	model = DeviceInstance
	form_class = DeviceInstanceForm
	template_name = 'submissions/deviceinstance_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class DeviceInstanceUpdateView(LoginRequiredMixin, UpdateView):
	model = DeviceInstance
	form_class = DeviceInstanceForm
	template_name = 'submissions/deviceinstance_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return DeviceInstance.objects.all()

class DeviceImplantCreateView(LoginRequiredMixin, CreateView):
	model = DeviceImplant
	form_class = DeviceImplantForm
	template_name = 'submissions/deviceimplant_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class DeviceImplantUpdateView(LoginRequiredMixin, UpdateView):
	model = DeviceImplant
	form_class = DeviceImplantForm
	template_name = 'submissions/deviceimplant_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return DeviceImplant.objects.all()

class DeviceEventCreateView(LoginRequiredMixin, CreateView):
	model = DeviceEvent
	form_class = DeviceEventForm
	template_name = 'submissions/deviceevent_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class DeviceEventUpdateView(LoginRequiredMixin, UpdateView):
	model = DeviceEvent
	form_class = DeviceEventForm
	template_name = 'submissions/deviceevent_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return DeviceEvent.objects.all()

class CoronaryInterventionCreateView(LoginRequiredMixin, CreateView):
	model = CoronaryIntervention
	form_class = CoronaryInterventionForm
	template_name = 'submissions/coronaryintervention_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class CoronaryInterventionUpdateView(LoginRequiredMixin, UpdateView):
	model = CoronaryIntervention
	form_class = CoronaryInterventionForm
	template_name = 'submissions/coronaryintervention_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return CoronaryIntervention.objects.all()

class ClinicalEventCreateView(LoginRequiredMixin, CreateView):
	model = ClinicalEvent
	form_class = ClinicalEventForm
	template_name = 'submissions/clinicalevent_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class ClinicalEventUpdateView(LoginRequiredMixin, UpdateView):
	model = ClinicalEvent
	form_class = ClinicalEventForm
	template_name = 'submissions/clinicalevent_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return ClinicalEvent.objects.all()

class Clinical_evaluationCreateView(LoginRequiredMixin, CreateView):
	model = Clinical_evaluation
	form_class = Clinical_evaluationForm
	template_name = 'submissions/clinical_evaluation_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Clinical_evaluationUpdateView(LoginRequiredMixin, UpdateView):
	model = Clinical_evaluation
	form_class = Clinical_evaluationForm
	template_name = 'submissions/clinical_evaluation_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Clinical_evaluation.objects.all()

class Ajmaline_testCreateView(LoginRequiredMixin, CreateView):
	model = Ajmaline_test
	form_class = AjmalineTestForm
	template_name = 'submissions/ajmaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Ajmaline_testUpdateView(LoginRequiredMixin, UpdateView):
	model = Ajmaline_test
	form_class = AjmalineTestForm
	template_name = 'submissions/ajmaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Ajmaline_test.objects.all()

class Ajmaline_testCreateView(LoginRequiredMixin, CreateView):
	model = Ajmaline_test
	form_class = AjmalineTestForm
	template_name = 'submissions/ajmaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Ajmaline_testUpdateView(LoginRequiredMixin, UpdateView):
	model = Ajmaline_test
	form_class = AjmalineTestForm
	template_name = 'submissions/ajmaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Ajmaline_test.objects.all()

class Adrenaline_testCreateView(LoginRequiredMixin, CreateView):
	model = Adrenaline_test
	form_class = AdrenalineTestForm
	template_name = 'submissions/adrenaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class Adrenaline_testUpdateView(LoginRequiredMixin, UpdateView):
	model = Adrenaline_test
	form_class = AdrenalineTestForm
	template_name = 'submissions/adrenaline_test_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Adrenaline_test.objects.all()

class AblationCreateView(LoginRequiredMixin, CreateView):
	model = Study
	form_class = StudyForm
	template_name = 'submissions/ablation_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class AblationUpdateView(LoginRequiredMixin, UpdateView):
	model = Ablation
	form_class = AblationForm
	template_name = 'submissions/ablation_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Ablation.objects.all()

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

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Late_potentials.objects.all()


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

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Late_potentials.objects.all()

class LatePotentialCreateView(LoginRequiredMixin, CreateView):
	model = Late_potentials
	form_class = LatePotentialForm
	template_name = 'submissions/latepotential_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class LatePotentialUpdateView(LoginRequiredMixin, UpdateView):
	model = Late_potentials
	form_class = LatePotentialForm
	template_name = 'submissions/latepotential_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return Late_potentials.objects.all()

class PatientProfileCreateView(LoginRequiredMixin, CreateView):
	model = PatientProfile
	form_class = PatientProfileForm
	template_name = 'submissions/patientprofile_form.html'
	success_url = reverse_lazy('submissions:submission_success')

class PatientProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = PatientProfile
	form_class = PatientProfileForm
	template_name = 'submissions/patientprofile_form.html'
	success_url = reverse_lazy('submissions:submission_success')

	def get_queryset(self):
		# Optional: limit which profiles a user can edit
		return PatientProfile.objects.all()