from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from kokoro.models import PatientProfile
from kokoro.forms import PatientProfileForm


class PatientProfileCreateView(LoginRequiredMixin, CreateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = 'submissions/patientprofile_form.html'
    success_url = reverse_lazy('submissions:submission_success')