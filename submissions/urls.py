from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
	path('patientprofile/add/', PatientProfileCreateView.as_view(), name='add_patientprofile'),

	# Optional success page after submission
	path('success/', TemplateView.as_view(
		template_name='submissions/success.html'
	), name='submission_success'),  
]