from django.urls import path
from .views import (KokoroHomeView, TherapyAutocomplete, AllergyAutocomplete,
					StudyAutocomplete, PatientProfileAutocomplete, PatientSpecificResearchView,
					AdvancedResearchView, RemoteMonirotingView, filter_counts_partial, PatientDetailView
				)

urlpatterns = [
    path('therapy-autocomplete/', TherapyAutocomplete.as_view(), name='therapy-autocomplete'),
    path('allergy-autocomplete/', AllergyAutocomplete.as_view(), name='allergy-autocomplete'),
    path('study-autocomplete/', StudyAutocomplete.as_view(), name='study-autocomplete'),
    path('patientprofile-autocomplete/', PatientProfileAutocomplete.as_view(), name='patientprofile-autocomplete'),
    path("patient-specific-research/", PatientSpecificResearchView.as_view(), name="patient-specific research"),
    path("advanced-research/", AdvancedResearchView.as_view(), name="advanced research"),
    path("remote-monitoring/", RemoteMonirotingView.as_view(), name="remote monitoring"),
    path("filter_counts/", filter_counts_partial, name="filter_counts_partial"),
	path("", KokoroHomeView.as_view(), name="kokoro_patient_list"),
	path("<uuid:pk>/", PatientDetailView.as_view(), name="patient_detail"),
]