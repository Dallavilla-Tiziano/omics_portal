from django.urls import path
# Importa le view dal file views.py della stessa app:
# PatientListView: vista per mostrare la lista di pazienti.
# PatientDetailView: vista per mostrare il dettaglio di un paziente.
# download_filtered_csv: vista per scaricare un file CSV filtrato.
# filter_counts_partial: vista che restituisce il conteggio dei filtri (di solito via AJAX).
from .views import PatientListView, PatientDetailView, download_filtered_csv, filter_counts_partial

urlpatterns = [
	path("", PatientListView.as_view(), name="patient_list"),
	path("<uuid:pk>/", PatientDetailView.as_view(), name="patient_detail"),
	path("reset/", PatientListView.as_view(), name="patient_reset"),
	path("download/", download_filtered_csv, name="patient_list_csv"),
	path("filter_counts/", filter_counts_partial, name="filter_counts_partial"),
]