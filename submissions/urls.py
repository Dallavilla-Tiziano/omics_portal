from django.urls import path
from django.views.generic import TemplateView
from .views import PatientProfileCreateView, PatientProfileUpdateView

app_name = 'submissions'

urlpatterns = [
	path('patientprofile/add/', PatientProfileCreateView.as_view(), name='add_patientprofile'),
    path('patientprofile/edit/<uuid:pk>/', PatientProfileUpdateView.as_view(), name='edit_patientprofile'),
	# Optional success page after submission
	path('success/', TemplateView.as_view(
		template_name='submissions/success.html'
	), name='submission_success'),  
]