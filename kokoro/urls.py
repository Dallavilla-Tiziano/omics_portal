from django.urls import path
from .views import KokoroHomeView, PatientSpecificResearchView, AdvancedResearchView, RemoteMonirotingView, filter_counts_partial

urlpatterns = [
	path("", KokoroHomeView.as_view(), name="kokoro_patient_list"),
    path("patient-specific-research/", PatientSpecificResearchView.as_view(), name="patient-specific research"),
    path("advanced-research/", AdvancedResearchView.as_view(), name="advanced research"),
    path("remote-monitoring/", RemoteMonirotingView.as_view(), name="remote monitoring"),
    path("filter_counts/", filter_counts_partial, name="filter_counts_partial"),
]