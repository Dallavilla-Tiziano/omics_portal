from django.urls import path
from .views import PatientListView, PatientDetailView, download_filtered_csv, filter_counts_partial

urlpatterns = [
	path("", PatientListView.as_view(), name="patient_list"),
	path("<uuid:pk>/", PatientDetailView.as_view(), name="patient_detail"),
	path("reset/", PatientListView.as_view(), name="patient_reset"),
	path("download/", download_filtered_csv, name="patient_list_csv"),
	path("filter_counts/", filter_counts_partial, name="filter_counts_partial"),
]