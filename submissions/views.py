from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from kokoro.models import (
						PatientProfile, Late_potentials, Study,
						Ablation, Adrenaline_test, Ajmaline_test,
						Clinical_evaluation, ClinicalEvent, CoronaryIntervention,
						DeviceEvent, DeviceImplant, DeviceInstance,
						EP_study, ECG, ECHO,
						Flecainide_test, Genetic_profile, Genetic_status,
						Genetic_test, RMN_TC_PH, Sample,
						ValveIntervention,
					)
from kokoro.forms import (
						PatientProfileForm, LatePotentialForm, StudyForm,
						AblationForm, AdrenalineTestForm, AjmalineTestForm,
						Clinical_evaluationForm, ClinicalEventForm, CoronaryInterventionForm,
						DeviceEventForm, DeviceImplantForm, DeviceInstanceForm,
						EP_studyForm, ECGForm, ECHOForm,
						Flecainide_testForm, Genetic_profileForm, Genetic_statusForm,
						Genetic_testForm, RMN_TC_PHTest, SampleForm,
						ValveInterventionForm,
					)

class AblationCreateView(LoginRequiredMixin, CreateView):
    model = Study
    form_class = StudyForm
    template_name = 'submissions/ablation_form.html'
    success_url = reverse_lazy('submissions:submission_success')

class AblationUpdateView(LoginRequiredMixin, UpdateView):
    model = Ablation
    form_class = AblationForm
    template_name = 'submissions/ablation_form.html'
    success_url = reverse_lazy('submissions:submission_success')

    def get_queryset(self):
        # Optional: limit which profiles a user can edit
        return Ablation.objects.all()

class StudyCreateView(LoginRequiredMixin, CreateView):
    model = Study
    form_class = StudyForm
    template_name = 'submissions/study_form.html'
    success_url = reverse_lazy('submissions:submission_success')

class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = Study
    form_class = StudyForm
    template_name = 'submissions/study_form.html'
    success_url = reverse_lazy('submissions:submission_success')

    def get_queryset(self):
        # Optional: limit which profiles a user can edit
        return Late_potentials.objects.all()


class StudyCreateView(LoginRequiredMixin, CreateView):
    model = Study
    form_class = StudyForm
    template_name = 'submissions/study_form.html'
    success_url = reverse_lazy('submissions:submission_success')

class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = Study
    form_class = StudyForm
    template_name = 'submissions/study_form.html'
    success_url = reverse_lazy('submissions:submission_success')

    def get_queryset(self):
        # Optional: limit which profiles a user can edit
        return Late_potentials.objects.all()

class LatePotentialCreateView(LoginRequiredMixin, CreateView):
    model = Late_potentials
    form_class = LatePotentialForm
    template_name = 'submissions/latepotential_form.html'
    success_url = reverse_lazy('submissions:submission_success')

class LatePotentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Late_potentials
    form_class = LatePotentialForm
    template_name = 'submissions/latepotential_form.html'
    success_url = reverse_lazy('submissions:submission_success')

    def get_queryset(self):
        # Optional: limit which profiles a user can edit
        return Late_potentials.objects.all()

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