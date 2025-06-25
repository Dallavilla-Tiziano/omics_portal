from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from kokoro.models import PatientProfile
from kokoro.forms import PatientProfileForm


class PatientProfileCreateView(LoginRequiredMixin, CreateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = 'submissions/patientprofile_form.html'
    success_url = reverse_lazy('submissions:submission_success')

class PatientProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = 'submissions/patientprofile_form.html'
    success_url = reverse_lazy('submissions:submission_success')

    def get_queryset(self):
        # Optional: limit which profiles a user can edit
        return PatientProfile.objects.all()