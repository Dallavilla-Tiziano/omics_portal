from django.urls import path
from .views import (KokoroHomeView, TherapyAutocomplete,
    AllergyAutocomplete, StudyAutocomplete, PatientProfileAutocomplete,
    PatientSpecificResearchView, AdvancedResearchView, RemoteMonitoringView,
    filter_counts_partial, PatientDetailView, SampleUpdateView,
    ClinicalEventUpdateView, DeviceInstanceUpdateView, DeviceEventUpdateView,
    AblationUpdateView,DeviceImplantUpdateView,ValveInterventionUpdateView,
    CoronaryInterventionUpdateView,ClinicalEvaluationUpdateView,AjmalineTestUpdateView,
    AdrenalineTestUpdateView,FlecainideTestUpdateView,EPStudyUpdateView,ECGUpdateView,ECHOUpdateView,
    LatePotentialsUpdateView,RMNTCPhUpdateView,GeneticProfileUpdateView,
    GeneticStatusUpdateView, GeneticTestUpdateView, #GeneticSampleUpdateView
    StudyUpdateView, TherapyUpdateView, ResearchAnalysisUpdateView, #PatientStudyUpdateView
    SymptomUpdateView,
)
  
app_name = "kokoro"

urlpatterns = [
    # Autocompletes & filters
    path('therapy-autocomplete/', TherapyAutocomplete.as_view(), name='therapy-autocomplete'),
    path('allergy-autocomplete/', AllergyAutocomplete.as_view(), name='allergy-autocomplete'),
    path('study-autocomplete/', StudyAutocomplete.as_view(), name='study-autocomplete'),
    path('patientprofile-autocomplete/', PatientProfileAutocomplete.as_view(), name='patientprofile-autocomplete'),
    path("filter_counts/", filter_counts_partial, name="filter_counts_partial"),

    # Research views
    path("", KokoroHomeView.as_view(), name="kokoro_patient_list"),
    path("patient-specific-research/", PatientSpecificResearchView.as_view(), name="patient-specific research"),
    path("advanced-research/", AdvancedResearchView.as_view(), name="advanced research"),
    path("remote-monitoring/", RemoteMonitoringView.as_view(), name="remote monitoring"),

    # Patient detail
    path("<uuid:pk>/", PatientDetailView.as_view(), name="patient_detail"),

    # Edit routes for every section
    path("sample/<uuid:pk>/edit/", SampleUpdateView.as_view(), name="sample-edit"),
    path("clinical-event/<int:pk>/edit/", ClinicalEventUpdateView.as_view(), name="clinicalevent-edit"),
    path("device-instance/<uuid:pk>/edit/", DeviceInstanceUpdateView.as_view(), name="deviceinstance-edit"),
    path("device-event/<uuid:pk>/edit/", DeviceEventUpdateView.as_view(), name="deviceevent-edit"),
    path("ablation/<uuid:pk>/edit/", AblationUpdateView.as_view(), name="ablation-edit"),
    path("device-implant/<uuid:pk>/edit/", DeviceImplantUpdateView.as_view(), name="deviceimplant-edit"),
    path("valve-intervention/<uuid:pk>/edit/", ValveInterventionUpdateView.as_view(), name="valveintervention-edit"),
    path("coronary-intervention/<uuid:pk>/edit/", CoronaryInterventionUpdateView.as_view(), name="coronaryintervention-edit"),
    path("clinical-evaluation/<uuid:pk>/edit/", ClinicalEvaluationUpdateView.as_view(), name="clinicalevaluation-edit"),
    path("ajmaline-test/<uuid:pk>/edit/", AjmalineTestUpdateView.as_view(), name="ajmalinetest-edit"),
    path("adrenaline-test/<uuid:pk>/edit/", AdrenalineTestUpdateView.as_view(), name="adrenalinetest-edit"),
    path("flecainide-test/<uuid:pk>/edit/", FlecainideTestUpdateView.as_view(), name="flecainidetest-edit"),
    path("ep-study/<uuid:pk>/edit/", EPStudyUpdateView.as_view(), name="epstudy-edit"),
    path("ecg/<uuid:pk>/edit/", ECGUpdateView.as_view(), name="ecg-edit"),
    path("echo/<uuid:pk>/edit/", ECHOUpdateView.as_view(), name="echo-edit"),
    path("late-potentials/<uuid:pk>/edit/", LatePotentialsUpdateView.as_view(), name="latepotentials-edit"),
    path("rmn-tc-ph/<uuid:pk>/edit/", RMNTCPhUpdateView.as_view(), name="rmn_tc_ph-edit"),
    path("genetic-profile/<uuid:pk>/edit/", GeneticProfileUpdateView.as_view(), name="geneticprofile-edit"),
    path("genetic-status/<uuid:pk>/edit/", GeneticStatusUpdateView.as_view(), name="geneticstatus-edit"),
    # path("genetic-sample/<uuid:pk>/edit/", GeneticSampleUpdateView.as_view(), name="geneticsample-edit"),
    path("genetic-test/<uuid:pk>/edit/", GeneticTestUpdateView.as_view(), name="genetictest-edit"),
    path("study/<uuid:pk>/edit/", StudyUpdateView.as_view(), name="study-edit"),
    path("therapy/<int:pk>/edit/", TherapyUpdateView.as_view(), name="therapy-edit"),
    # path("patient-study/<uuid:pk>/edit/", PatientStudyUpdateView.as_view(), name="patientstudy-edit"),
    path("research-analysis/<uuid:pk>/edit/", ResearchAnalysisUpdateView.as_view(), name="researchanalysis-edit"),
    path("symptoms/<int:pk>/edit/", SymptomUpdateView.as_view(), name="symptom-edit"),
]
