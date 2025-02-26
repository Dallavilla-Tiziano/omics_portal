from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	PermissionRequiredMixin
	)
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import DetailView
from django.http import HttpResponse
from .models import Patient
from .tables import PatientTable
from .filters import PatientFilter
import csv


class PatientListView(LoginRequiredMixin, SingleTableMixin, FilterView):
	model = Patient
	table_class = PatientTable
	context_object_name = "patient_list"
	template_name = "patients/patient_list.html"
	login_url = "account_login"
	filterset_class = PatientFilter

	def get_queryset(self):
		queryset = super().get_queryset()
		# If 'reset' is in the query params, return all patients (no filtering)
		rows_per_page = self.request.GET.get("rows_per_page", "20")
		if "reset" in self.request.GET:
			return Patient.objects.all()
		return queryset

	def render_to_response(self, context, **response_kwargs):
		"""✅ Detect HTMX requests correctly and return only the table."""
		if self.request.headers.get("HX-Request") == "true":
			return render(self.request, "patients/_table.html", context, **response_kwargs)
		return super().render_to_response(context, **response_kwargs)

	def get_table_pagination(self, table):
		rows_per_page = self.request.GET.get("rows", 20)  # Default is 20 rows
		return {"per_page": rows_per_page}

class PatientDetailView(
						LoginRequiredMixin,
						PermissionRequiredMixin,
						DetailView):
	model = Patient
	context_object_name = "patient"
	template_name = "patients/patient_detail.html"
	login_url = "account_login"
	permission_required = "patients.access_sensible_info"

def download_filtered_csv(request):
    """Generate a CSV file with the currently filtered patient data"""

    # Check if the request contains filters
    print("GET Parameters:", request.GET)  # Debugging step

    # Apply filters to only retrieve the filtered data
    filtered_patients = PatientFilter(request.GET, queryset=Patient.objects.all()).qs

    # Debugging step: Print filtered patient count
    print("Filtered Patients Count:", filtered_patients.count())

    # Create the response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="filtered_patients.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(["Last Name", "First Name", "Date of Birth", "Sex", "Status", "Nation"])

    # Write patient data
    for patient in filtered_patients:
        writer.writerow([patient.last_name, patient.first_name, patient.date_of_birth, 
                         patient.sex, patient.patient_type, patient.nation])

    return response