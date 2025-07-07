from dal import autocomplete
from django.views.generic import DetailView, UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
import pandas as pd
import json

from kokoro.models import (
	PatientProfile, Sample, ClinicalEvent, DeviceInstance, DeviceEvent,
	Ablation, DeviceImplant, ValveIntervention, CoronaryIntervention,
	Therapy, Study, PatientStudy, ResearchAnalysis, Clinical_evaluation,
	EP_study, Flecainide_test, Adrenaline_test, Ajmaline_test,
	ECG, ECHO, Late_potentials, RMN_TC_PH,
	Genetic_profile, Genetic_status, Genetic_sample, Genetic_test, Symptoms, ResearchAnalysis
)

from kokoro.forms import (
						PatientProfileForm, LatePotentialForm, StudyForm,
						AblationForm, AdrenalineTestForm, AjmalineTestForm,
						Clinical_evaluationForm, ClinicalEventForm, CoronaryInterventionForm,
						DeviceEventForm, DeviceImplantForm, DeviceInstanceForm,
						EP_studyForm, ECGForm, ECHOForm,
						Flecainide_testForm, Genetic_profileForm, Genetic_statusForm,
						Genetic_testForm, RMN_TC_PHTest, SampleForm,
						ValveInterventionForm, TherapyForm, ResearchAnalysisForm
					)

from .tables import PatientTable
from .filters import DemographicFilter
from .query_helpers import get_filtered_patients
import csv

class TherapyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Therapy.objects.all()
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(name__icontains=search)
		return qs

class AllergyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Therapy.objects.all()
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(name__icontains=search)
		return qs

class StudyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Study.objects.all()
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(project_code__icontains=search)
		return qs

class PatientProfileAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = PatientProfile.objects.all()
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(
				Q(last_name__icontains=search) |
				Q(first_name__icontains=search) |
				Q(cardioref_id__icontains=search)
			)
		return qs


def get_filter_counts(request):
	filtered_patients = get_filtered_patients(request)
	return {"patients": filtered_patients.count()}

class KokoroHomeView(LoginRequiredMixin, SingleTableMixin, FilterView):
	model = PatientProfile
	table_class = PatientTable
	context_object_name = "kokoro_patient_list"
	template_name = "kokoro/kokoro.html"
	login_url = "account_login"

class PatientSpecificResearchView(LoginRequiredMixin, SingleTableMixin, FilterView):
	model = PatientProfile
	table_class = PatientTable
	# context_object_name = "patient-specific research"
	template_name = "kokoro/patient-specific research.html"
	login_url = "account_login"

	def get_queryset(self):
		# Start with base queryset
		qs = PatientProfile.objects.all()

		# Apply demographic filter
		self.demographic_filter = DemographicFilter(self.request.GET, queryset=qs)
		qs = self.demographic_filter.qs

		# Future: apply other filters here
		# self.sample_filter = SampleFilter(self.request.GET, queryset=qs)
		# qs = self.sample_filter.qs

		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# Reuse filters from get_queryset (already applied)
		context["demographic_filter"] = getattr(self, "demographic_filter", DemographicFilter(self.request.GET))
		# context["sample_filter"] = getattr(self, "sample_filter", SampleFilter(self.request.GET))
		context["filter_counts"] = get_filter_counts(self.request)

		return context

	def render_to_response(self, context, **response_kwargs):
		if self.request.headers.get("HX-Request"):
			return render(self.request, "kokoro/_table.html", context)
		return super().render_to_response(context, **response_kwargs)

	def get_table_pagination(self, table):
		rows = self.request.GET.get("rows", "20")
		if self.request.GET.get("paginate") == "false":
			return False
		try:
			return {"per_page": int(rows)}
		except ValueError:
			return {"per_page": 20}


class AdvancedResearchView(LoginRequiredMixin, SingleTableMixin, FilterView):
	model = PatientProfile
	table_class = PatientTable
	context_object_name = "advanced research"
	template_name = "kokoro/advanced research.html"
	login_url = "account_login"

class RemoteMonitoringView(LoginRequiredMixin, SingleTableMixin, FilterView):
	model = PatientProfile
	table_class = PatientTable
	context_object_name = "remote monitoring"
	template_name = "kokoro/remote monitoring.html"
	login_url = "account_login"

class PatientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = PatientProfile
	context_object_name = "patient"
	template_name = "kokoro/patient_detail.html"
	permission_required = "kokoro.access_sensible_info"
	login_url = "account_login"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		p = self.object

		# Direct relationships
		ctx["samples"]             = p.samples.all()
		ctx["research_analyses"]   = ResearchAnalysis.objects.filter(samples__patient=p).distinct()
		ctx["clinical_events"]     = p.clinical_event.all()
		ctx["clinical_evaluations"] = p.clinical_evaluation_set.all()
		ctx["devices"]             = p.patient.all()
		ctx["device_events"]       = DeviceEvent.objects.filter(device__patient=p)

		# Procedures
		ctx["ablations"]           = p.ablation_set.all()
		ctx["device_implants"]     = p.deviceimplant_set.all()
		ctx["valve_interventions"] = p.valveintervention_set.all()
		ctx["coronary_interventions"] = p.coronaryintervention_set.all()

		# Therapies & studies
		ctx["therapies"]           = p.therapies.all()
		ctx["allergies"]           = p.allergies.all()
		ctx["studies"]             = p.studies.all()
		ctx["patient_studies"]     = p.patient_studies.all()

		# Provocative tests
		ctx["ep_studies"]          = p.ep_study_set.all()
		ctx["flecainide_tests"]    = p.flecainide_test_set.all()
		ctx["adrenaline_tests"]    = p.adrenaline_test_set.all()
		ctx["ajmaline_tests"]      = p.ajmaline_test_set.all()

		# Diagnostic exams
		ctx["ecgs"]                = p.ecg_set.all()
		ctx["echos"]               = p.echo_set.all()
		ctx["late_potentials"]     = p.late_potentials_set.all()
		ctx["rmn_tc_ph"]           = p.rmn_tc_ph_set.all()

		# Genetics
		ctx["genetic_profiles"]    = p.genetic_profile_set.all()
		ctx["genetic_statuses"]    = p.genetic_status_set.all()
		ctx["genetic_samples"]     = p.genetic_sample_set.all()
		ctx["genetic_tests"]       = p.genetic_test_set.all()

		# ECG plot data
		ecg_data = []
		for ecg in ctx["ecgs"]:
			if ecg.ecg_file:
				try:
					path = ecg.ecg_file.path
					df = pd.read_csv(path, header=None)
					if df.shape[1] == 13:
						df.columns = [
							"time", "I", "II", "III", "aVR", "aVL", "aVF",
							"V1", "V2", "V3", "V4", "V5", "V6"
						]
						df["time"] = df["time"] / 2000.0  # ✅ Fix: milliseconds to seconds
						lead_cols = [
							"I", "II", "III", "aVR", "aVL", "aVF",
							"V1", "V2", "V3", "V4", "V5", "V6"
						]
						df[lead_cols] = df[lead_cols] / 1000.0  # ✅ Fix: convert to millivolts
						df = df.sort_values(by="time")

						ecg_data.append({
							"id": str(ecg.id),
							"label": str(ecg),  # or ecg.date_of_exam
							"data": json.dumps(df.to_dict(orient="records")),
						})
				except Exception as e:
					print(f"Failed to parse ECG CSV for ECG {ecg.id}: {e}")

		ctx["ecg_plot_data"] = ecg_data
		return ctx

class SymptomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Therapy
	form_class = TherapyForm
	template_name = "submissions/symptom_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.pk])

class ResearchAnalysisUpdateView(LoginRequiredMixin,
                                 PermissionRequiredMixin,
                                 UpdateView):
    model = ResearchAnalysis
    form_class = ResearchAnalysisForm
    template_name = "submissions/research_analysis_form.html"
    permission_required = "kokoro.access_sensible_info"

    def get_success_url(self):
        # Pick the first sample on this analysis
        first_sample = self.object.samples.first()
        if not first_sample:
            # No samples? send back to the patient list
            return reverse_lazy("kokoro:kokoro_patient_list")
        # Assume Sample has `patient` FK to PatientProfile
        patient_id = first_sample.patient_id
        return reverse_lazy(
            "kokoro:patient_detail",
            kwargs={"pk": patient_id}
        )

# class TherapyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
# 	model = Therapy
# 	form_class = TherapyForm
# 	template_name = "submissions/therapy_form.html"
# 	permission_required = "kokoro.access_sensible_info"

# 	def get_success_url(self):
# 		return reverse_lazy("kokoro:patient_detail", args=[self.object.pk])

class PatientTherapiesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PatientProfile
    fields = ["therapies"]            # only the M2M field
    template_name = "submissions/therapy_form.html"
    permission_required = "kokoro.access_sensible_info"

    def get_success_url(self):
        # now `self.object` *is* a patient, so this works:
        return reverse_lazy("kokoro:patient_detail",
                            kwargs={"pk": self.object.pk})

class PatientProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = PatientProfile
	form_class = PatientProfileForm
	template_name = "submissions/patientprofile_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.pk])

class SampleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Sample
	template_name = "submissions/sample_form.html"
	form_class = SampleForm     # ← tell Django which ModelForm to use

	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
	 return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class ClinicalEventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = ClinicalEvent
	form_class = ClinicalEventForm
	template_name = "submissions/clinicalevent_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class ClinicalEvaluationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Clinical_evaluation
	form_class = Clinical_evaluationForm
	template_name = "submissions/clinicalevent_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class DeviceEventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = DeviceEvent
	form_class = DeviceEventForm
	template_name = "submissions/deviceevent_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.device.patient.pk])

class DeviceInstanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = DeviceInstance
	form_class = DeviceInstanceForm
	template_name = "submissions/deviceinstance_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class AblationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Ablation
	form_class = AblationForm
	template_name = "submissions/ablation_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class DeviceImplantUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = DeviceImplant
	form_class = DeviceImplantForm
	template_name = "submissions/deviceimplant_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class ValveInterventionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = ValveIntervention
	form_class = ValveInterventionForm
	template_name = "submissions/valveintervention_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class CoronaryInterventionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = CoronaryIntervention
	form_class = CoronaryInterventionForm
	template_name = "submissions/coronaryintervention_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class AdrenalineTestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Adrenaline_test
	form_class = AdrenalineTestForm
	template_name = "submissions/adrenaline_test_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class AjmalineTestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Ajmaline_test
	form_class = AjmalineTestForm
	template_name = "submissions/ajmaline_test_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class FlecainideTestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Flecainide_test
	form_class = Flecainide_testForm
	template_name = "submissions/flecainide_test_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class RMNTCPhUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = RMN_TC_PH
	form_class = RMN_TC_PHTest
	template_name = "submissions/rmn_tc_phtest_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class ECGUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = ECG
	form_class = ECGForm
	template_name = "submissions/ecg_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class ECHOUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = ECHO
	form_class = ECHOForm
	template_name = "submissions/echo_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class EPStudyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = EP_study
	form_class = EP_studyForm
	template_name = "submissions/ep_study_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class StudyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Study
	form_class = StudyForm
	template_name = "submissions/study_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class LatePotentialsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Late_potentials
	form_class = LatePotentialForm
	template_name = "submissions/late_potential_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class GeneticProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Genetic_profile
	form_class = Genetic_profileForm
	template_name = "submissions/genetic_profile_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class GeneticStatusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Genetic_status
	form_class = Genetic_statusForm
	template_name = "submissions/genetic_status_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

class GeneticTestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Genetic_test
	form_class = Genetic_testForm
	template_name = "submissions/genetic_test_form.html"
	permission_required = "kokoro.access_sensible_info"

	def get_success_url(self):
		return reverse_lazy("kokoro:patient_detail", args=[self.object.patient.pk])

def filter_counts_partial(request):
	return render(request, "kokoro/filter_counts.html", {"filter_counts": get_filter_counts(request)})

def download_filtered_csv(request):
	# Get the filtered patients once and prefetch related samples and analyses.
	filtered_patients_qs = get_filtered_patients(request).prefetch_related("samples", "samples__analyses")
	# Convert the queryset to a list to avoid re-querying.
	filtered_patients = list(filtered_patients_qs)
	
	# Compute filtered sample and analysis IDs by iterating over the already prefetched data.
	filtered_sample_ids = {
		sample.id
		for patient in filtered_patients
		for sample in patient.samples.all()
	}

	filtered_analysis_ids = {
		analysis.id
		for patient in filtered_patients
		for sample in patient.samples.all()
		for analysis in sample.analyses.all()
	}
	
	response = HttpResponse(content_type="text/csv")
	response["Content-Disposition"] = 'attachment; filename="filtered_patients_with_samples_and_analyses.csv"'
	writer = csv.writer(response)
	writer.writerow([
		"Patient UUID", "Last Name", "First Name", "Date of Birth", "Sex", "Nation",
		"Sample UUID", "Sample ID", "Sample Type", "Collection Date", "Sample Status",
		"Analysis Type", "Date Performed", "Result Files"
	])
	
	# Iterate over filtered patients
	for patient in filtered_patients:
		# Get only those samples whose IDs are in the filtered set.
		valid_samples = [sample for sample in patient.samples.all() if sample.id in filtered_sample_ids]
		if valid_samples:
			for sample in valid_samples:
				# For each sample, get only those analyses whose IDs are in the filtered set.
				valid_analyses = [analysis for analysis in sample.analyses.all() if analysis.id in filtered_analysis_ids]
				if valid_analyses:
					for analysis in valid_analyses:
						writer.writerow([
							patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
							patient.sex, patient.nation,
							sample.id, sample.collection_date,
							analysis.type, analysis.date_performed, analysis.result_files
						])
				else:
					# Write row if sample has no valid analyses.
					writer.writerow([
						patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
						patient.sex, patient.nation,
						sample.id, sample.collection_date,
						"None", "None", "None"
					])
		else:
			# Write a row with patient info if there are no valid samples.
			writer.writerow([
				patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
				patient.sex, patient.nation,
				"None", "None", "None", "None", "None", "None",
				"None", "None", "None"
			])
	return response