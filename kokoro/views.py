from django.views.generic import TemplateView

class KokoroHome(TemplateView):
	template_name = "kokoro/kokoro.html"

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.http import HttpResponse
from .models import PatientProfile
from .tables import PatientTable
from .filters import DemographicFilter
from .query_helpers import get_filtered_patients
import csv

def get_filter_counts(request):
    """
    Returns a dictionary with the counts of filtered patients, samples, and analyses.
    """
    filtered_patients = get_filtered_patients(request)
    return {
        "patients": filtered_patients.count(),
    }

class PatientListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = PatientProfile
    table_class = PatientTable
    context_object_name = "patient_list"
    template_name = "patients/patient_list.html"
    login_url = "account_login"

    def get_queryset(self):
        # Use the unified filtering helper to build the queryset.
        return get_filtered_patients(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demographic_filter"] = DemographicFilter(self.request.GET, queryset=PatientProfile.objects.all())
        context["filter_counts"] = get_filter_counts(self.request)
        return context

    def render_to_response(self, context, **response_kwargs):
        # If the request is from HTMX, render only the table partial.
        if self.request.headers.get("HX-Request"):
            return render(self.request, "patients/_table.html", context)
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

class PatientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = PatientProfile
    context_object_name = "patient"
    template_name = "patients/patient_detail.html"
    login_url = "account_login"
    permission_required = "patients.access_sensible_info"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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
    return render(request, "patients/filter_counts.html", {"filter_counts": filter_counts})
