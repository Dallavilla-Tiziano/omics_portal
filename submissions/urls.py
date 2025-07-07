from django.urls import path
from django.views.generic import TemplateView
from .views import (
	PatientProfileCreateView, PatientProfileUpdateView,
	AblationCreateView, AblationUpdateView,
	Adrenaline_testCreateView, Adrenaline_testUpdateView,
	Ajmaline_testCreateView, Ajmaline_testUpdateView,
	ClinicalEventCreateView, ClinicalEventUpdateView,
	Clinical_evaluationCreateView, Clinical_evaluationUpdateView,
	CoronaryInterventionCreateView, CoronaryInterventionUpdateView,
	DeviceInstanceCreateView, DeviceInstanceUpdateView,
	DeviceImplantCreateView, DeviceImplantUpdateView,
	DeviceEventCreateView, DeviceEventUpdateView,
	ECGCreateView, ECGUpdateView,
	ECHOCreateView, ECHOUpdateView,
	EP_studyCreateView, EP_studyUpdateView,
	Flecainide_testCreateView, Flecainide_testUpdateView,
	Genetic_profileCreateView, Genetic_profileUpdateView,
	Genetic_statusCreateView, Genetic_statusUpdateView,
	Genetic_testCreateView, Genetic_testUpdateView,
	LatePotentialCreateView, LatePotentialUpdateView,
	ResearchAnalysisCreateView,
	RMN_TC_PHCreateView, RMN_TC_PHUpdateView,
	SampleCreateView, SampleUpdateView,
	StudyCreateView, StudyUpdateView,
	ValveInterventionCreateView, ValveInterventionUpdateView,
	ParentSearchView, ChildTypeListView
)

app_name = 'submissions'

urlpatterns = [
	# Parent selection
	path('new/', ParentSearchView.as_view(), name='submission'),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/',
		ChildTypeListView.as_view(),
		name='submission_children'
	),

	# Create routes with parent context
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/ablation/add/',
		AblationCreateView.as_view(),
		name='add_ablation'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/adrenaline_test/add/',
		Adrenaline_testCreateView.as_view(),
		name='add_adrenaline_test'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/ajmaline_test/add/',
		Ajmaline_testCreateView.as_view(),
		name='add_ajmaline_test'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/clinicalevent/add/',
		ClinicalEventCreateView.as_view(),
		name='add_clinicalevent'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/clinical_evaluation/add/',
		Clinical_evaluationCreateView.as_view(),
		name='add_clinical_evaluation'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/coronaryintervention/add/',
		CoronaryInterventionCreateView.as_view(),
		name='add_coronaryintervention'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/deviceinstance/add/',
		DeviceInstanceCreateView.as_view(),
		name='add_deviceinstance'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/deviceimplant/add/',
		DeviceImplantCreateView.as_view(),
		name='add_deviceimplant'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/deviceevent/add/',
		DeviceEventCreateView.as_view(),
		name='add_deviceevent'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/ecg/add/',
		ECGCreateView.as_view(),
		name='add_ecg'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/echo/add/',
		ECHOCreateView.as_view(),
		name='add_echo'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/ep_study/add/',
		EP_studyCreateView.as_view(),
		name='add_ep_study'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/flecainide_test/add/',
		Flecainide_testCreateView.as_view(),
		name='add_flecainide_test'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/latepotential/add/',
		LatePotentialCreateView.as_view(),
		name='add_latepotential'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/genetic_profile/add/',
		Genetic_profileCreateView.as_view(),
		name='add_genetic_profile'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/genetic_status/add/',
		Genetic_statusCreateView.as_view(),
		name='add_genetic_status'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/genetic_test/add/',
		Genetic_testCreateView.as_view(),
		name='add_genetic_test'
	),
	path(
		'new/<str:parent_type>/<uuid:parent_id>/children/sample/add/',
		SampleCreateView.as_view(),
		name='add_sample'
	),

	# Sample-specific children
	path(
		'new/sample/<uuid:parent_id>/children/researchanalysis/add/',
		ResearchAnalysisCreateView.as_view(),
		name='add_researchanalysis'
	),

	# Study-specific children (enrollment)
	path(
		'new/study/<uuid:parent_id>/children/studyenrollment/add/',
		StudyCreateView.as_view(),
		name='add_patientstudy'
	),
	
    path(
        'new/<str:parent_type>/<uuid:parent_id>/children/valveintervention/add/',
        ValveInterventionCreateView.as_view(),
        name='add_valveintervention'
    ),

	# Standalone create/edit routes without parent context
	path('patientprofile/add/', PatientProfileCreateView.as_view(), name='add_patientprofile'),
	path('patientprofile/edit/<uuid:pk>/', PatientProfileUpdateView.as_view(), name='edit_patientprofile'),
	path('ablation/edit/<uuid:pk>/', AblationUpdateView.as_view(), name='edit_ablation'),
	path('adrenaline_test/edit/<uuid:pk>/', Adrenaline_testUpdateView.as_view(), name='edit_adrenaline_test'),
	path('ajmaline_test/edit/<uuid:pk>/', Ajmaline_testUpdateView.as_view(), name='edit_ajmaline_test'),
	path('clinicalevent/edit/<uuid:pk>/', ClinicalEventUpdateView.as_view(), name='edit_clinicalevent'),
	path('clinical_evaluation/edit/<uuid:pk>/', Clinical_evaluationUpdateView.as_view(), name='edit_clinical_evaluation'),
	path('coronaryintervention/edit/<uuid:pk>/', CoronaryInterventionUpdateView.as_view(), name='edit_coronaryintervention'),
	path('deviceinstance/edit/<uuid:pk>/', DeviceInstanceUpdateView.as_view(), name='edit_deviceinstance'),
	path('deviceimplant/edit/<uuid:pk>/', DeviceImplantUpdateView.as_view(), name='edit_deviceimplant'),
	path('deviceevent/edit/<uuid:pk>/', DeviceEventUpdateView.as_view(),
		name='edit_deviceevent'),
	path('ecg/edit/<uuid:pk>/', ECGUpdateView.as_view(), name='edit_ecg'),
	path('echo/edit/<uuid:pk>/', ECHOUpdateView.as_view(), name='edit_echo'),
	path('ep_study/edit/<uuid:pk>/', EP_studyUpdateView.as_view(), name='edit_ep_study'),
	path('flecainide_test/edit/<uuid:pk>/', Flecainide_testUpdateView.as_view(), name='edit_flecainide_test'),
	path('latepotential/edit/<uuid:pk>/', LatePotentialUpdateView.as_view(), name='edit_latepotential'),
	path('genetic_profile/edit/<uuid:pk>/', Genetic_profileUpdateView.as_view(), name='edit_genetic_profile'),
	path('genetic_status/edit/<uuid:pk>/', Genetic_statusUpdateView.as_view(), name='edit_genetic_status'),
	path('genetic_test/edit/<uuid:pk>/', Genetic_testUpdateView.as_view(), name='edit_genetic_test'),
	path('rmn_tc_ph/edit/<uuid:pk>/', RMN_TC_PHUpdateView.as_view(), name='edit_rmn_tc_ph'),
	path('sample/edit/<uuid:pk>/', SampleUpdateView.as_view(), name='edit_sample'),
	path('study/edit/<uuid:pk>/', StudyUpdateView.as_view(), name='edit_study'),
	path('valveintervention/edit/<uuid:pk>/', ValveInterventionUpdateView.as_view(), name='edit_valveintervention'),

	# Success page
	path('success/', TemplateView.as_view(template_name='submissions/success.html'), name='submission_success'),
]
