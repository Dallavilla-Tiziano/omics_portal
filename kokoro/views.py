from dal import autocomplete
from django.views.generic import TemplateView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    PatientProfile,
    Sample,
    ClinicalEvent,
    DeviceInstance,
    DeviceEvent,
    Ablation,
    DeviceImplant,
    ValveIntervention,
    CoronaryIntervention,
    Therapy,
    Study,
    PatientStudy,
    ResearchAnalysis,
    Clinical_evaluation,
    EP_study,
    Flecainide_test,
    Adrenaline_test,
    Ajmaline_test,
    ECG,
    ECHO,
    Late_potentials,
    RMN_TC_PH,
    Genetic_profile,
    Genetic_status,
    Genetic_sample,
    Genetic_test,
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
            qs = qs.filter(name__icontains=search)
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
    return {
        "patients": filtered_patients.count(),
    }

class KokoroHomeView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = PatientProfile
    table_class = PatientTable
    context_object_name = "kokoro_patient_list"
    template_name = "kokoro/kokoro.html"
    login_url = "account_login"

class PatientSpecificResearchView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = PatientProfile
    table_class = PatientTable
    context_object_name = "patient-specific research"
    template_name = "kokoro/patient-specific research.html"
    login_url = "account_login"

    def get_queryset(self):
        return get_filtered_patients(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demographic_filter"] = DemographicFilter(self.request.GET, queryset=PatientProfile.objects.all())
        context["filter_counts"] = get_filter_counts(self.request)
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("HX-Request"):
            return render(self.request, "kokoro/_table.html", context)
        return super().render_to_response(context, **response_kwargs)

    def get_table_pagination(self, table):
        rows_per_page = self.request.GET.get("rows", "20")
        if self.request.GET.get("paginate") == "false":
            return False
        try:
            rows_per_page = int(rows_per_page)
            return {"per_page": rows_per_page}
        except ValueError:
            return {"per_page": 20}

class AdvancedResearchView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = PatientProfile
    table_class = PatientTable
    context_object_name = "advanced research"
    template_name = "kokoro/advanced research.html"
    login_url = "account_login"

class RemoteMonirotingView(LoginRequiredMixin, SingleTableMixin, FilterView):
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

        # Direct M2M & FK relations
        ctx["samples"] = p.samples.all()
        ctx["clinical_events"] = p.clinical_event.all()
        ctx["devices"] = p.patient.all()
        ctx["device_events"] = DeviceEvent.objects.filter(device__patient=p)

        # Procedures
        ctx["ablations"] = p.ablation_set.all()
        ctx["device_implants"] = p.deviceimplant_set.all()
        ctx["valve_interventions"] = p.valveintervention_set.all()
        ctx["coronary_interventions"] = p.coronaryintervention_set.all()

        # Therapies, Allergies, Studies
        ctx["therapies"] = p.therapies.all()
        ctx["allergies"] = p.allergies.all()
        ctx["studies"] = p.studies.all()
        ctx["patient_studies"] = p.patient_studies.all()

        # Research analyses (via Sample → ResearchAnalysis)
        ctx["research_analyses"] = ResearchAnalysis.objects.filter(samples__patient=p).distinct()

        # Provocative tests
        ctx["ep_studies"] = p.ep_study_set.all()
        ctx["flecainide_tests"] = p.flecainide_test_set.all()
        ctx["adrenaline_tests"] = p.adrenaline_test_set.all()
        ctx["ajmaline_tests"] = p.ajmaline_test_set.all()

        # Diagnostic exams
        ctx["ecgs"] = p.ecg_set.all()
        ctx["echos"] = p.echo_set.all()
        ctx["late_potentials"] = p.late_potentials_set.all()
        ctx["rmn_tc_ph"] = p.rmn_tc_ph_set.all()

        # Genetics
        ctx["genetic_profiles"] = p.genetic_profile_set.all()
        ctx["genetic_statuses"] = p.genetic_status_set.all()
        ctx["genetic_samples"] = p.genetic_sample_set.all()
        ctx["genetic_tests"] = p.genetic_test_set.all()

        # Clinical evaluations
        ctx["clinical_evaluations"] = p.clinical_evaluation_set.all()

        return ctx



#def download_filtered_csv(request):
#    # Get the filtered patients once and prefetch related samples and analyses.
#    filtered_patients_qs = get_filtered_patients(request).prefetch_related("samples", "samples__analyses")
#    # Convert the queryset to a list to avoid re-querying.
#    filtered_patients = list(filtered_patients_qs)
	
	# Compute filtered sample and analysis IDs by iterating over the already prefetched data.
#    filtered_sample_ids = { sample.id for patient in filtered_patients for sample in patient.samples.all() }
#    filtered_analysis_ids = { analysis.id for patient in filtered_patients for sample in patient.samples.all() for analysis in sample.analyses.all() }
	
#    response = HttpResponse(content_type="text/csv")
#    response["Content-Disposition"] = 'attachment; filename="filtered_patients_with_samples_and_analyses.csv"'
#    writer = csv.writer(response)
#    writer.writerow([
#        "Patient UUID", "Last Name", "First Name", "Date of Birth", "Sex", "Patient Type", "Nation",
#        "Sample UUID", "Sample ID", "Sample Type", "Collection Date", "Storage Location", "Sample Status",
#        "Analysis Type", "Date Performed", "Result Files"
#    ])
	
	#######
	# Iterate over filtered patients
	#for patient in filtered_patients:
	#    # Get only those samples whose IDs are in the filtered set.
	#    valid_samples = [sample for sample in patient.samples.all() if sample.id in filtered_sample_ids]
	#    if valid_samples:
	#        for sample in valid_samples:
	#            # For each sample, get only those analyses whose IDs are in the filtered set.
	#            valid_analyses = [analysis for analysis in sample.analyses.all() if analysis.id in filtered_analysis_ids]
	#            if valid_analyses:
	#                for analysis in valid_analyses:
	#                    writer.writerow([
	#                        patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
	#                        patient.sex, patient.patient_type, patient.nation,
	#                        sample.id, sample.internal_id, sample.type, sample.collection_date,
	#                        sample.freezer_location, sample.get_status_display(),
	#                        analysis.type, analysis.date_performed, analysis.result_files
	#                    ])
	#            else:
	#                # Write row if sample has no valid analyses.
	#                writer.writerow([
	#                    patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
	#                    patient.sex, patient.patient_type, patient.nation,
	#                    sample.id, sample.internal_id, sample.type, sample.collection_date,
	#                    sample.freezer_location, sample.get_status_display(),
	#                    "None", "None", "None"
	#                ])
	#    else:
	#        # Write a row with patient info if there are no valid samples.
	#        writer.writerow([
	#            patient.id, patient.last_name, patient.first_name, patient.date_of_birth,
	#            patient.sex, patient.patient_type, patient.nation,
	#            "None", "None", "None", "None", "None", "None",
	#            "None", "None", "None"
	#        ])
	#return response

def filter_counts_partial(request):
	"""
	Returns a partial template with updated filter counts.
	"""
	filter_counts = get_filter_counts(request)
	return render(request, "kokoro/filter_counts.html", {"filter_counts": filter_counts})
