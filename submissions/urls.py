from django.urls import path
from django.views.generic import TemplateView
from .views import (PatientProfileCreateView, PatientProfileUpdateView, LatePotentialCreateView,
					LatePotentialUpdateView, StudyCreateView, StudyUpdateView
				)

app_name = 'submissions'

urlpatterns = [
	path('study/add/', StudyCreateView.as_view(), name='add_studyl'),
    path('study/edit/<uuid:pk>/', StudyUpdateView.as_view(), name='edit_study'),
	path('latepotential/add/', LatePotentialCreateView.as_view(), name='add_latepotential'),
    path('latepotential/edit/<uuid:pk>/', LatePotentialUpdateView.as_view(), name='edit_latepotential'),
	path('patientprofile/add/', PatientProfileCreateView.as_view(), name='add_patientprofile'),
    path('patientprofile/edit/<uuid:pk>/', PatientProfileUpdateView.as_view(), name='edit_patientprofile'),
	# Optional success page after submission
	path('success/', TemplateView.as_view(
		template_name='submissions/success.html'
	), name='submission_success'),  
]