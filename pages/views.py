from django.views.generic import TemplateView  # used to display an HTML template, useful for static or semi-static pages like homepage, about, etc.
from django.shortcuts import redirect  # used to redirect the user to another page. Here it's used to send unauthenticated users to the login page.
from django.db.models import Count  # a Django function useful to count objects directly at the database query level.
from collections import Counter  # Python class used to count occurrences of elements in a list or iterable. It is used to calculate distributions (e.g., how many patients per nation, sex, etc.).
import json
from kokoro.models import PatientProfile, ProcedureBase
from patients.models import Patient, Sample, Analysis


class HomePageView(TemplateView):
    template_name = "home.html"

    # Redirect to login if user is not authenticated
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get total counts
        #total_patients = Patient.objects.count()
        #total_samples = Sample.objects.count()
        #total_analysis = Analysis.objects.count()

        ### NEW ###
        total_patientProfiles = PatientProfile.objects.count()
        print(total_patientProfiles)
        #total_procedures = ProcedureBase.objects.count()

        # Get distribution data
        nationProfiles_counts = PatientProfile.objects.values_list("nation", flat=True)
        #sex_counts = Patient.objects.values_list("sex", flat=True)
        dobProfiles_years = PatientProfile.objects.values_list("date_of_birth", flat=True)

        ### NEW ###
        sexProfiles_counts = PatientProfile.objects.values_list("sex", flat=True)

        # Process distributions
        nationProfiles_distribution = dict(Counter(nationProfiles_counts))
        #sex_distribution = dict(Counter(sex_counts))
        dob_distribution = dict(Counter(d.year for d in dobProfiles_years if d))  # Group by birth year

        ### NEW ###
        sexProfiles_distribution = dict(Counter(sexProfiles_counts))

        # Add data to context
        #context.update({
        #    "total_patients": total_patients,
        #    "total_samples": total_samples,
        #    "total_analysis": total_analysis,
        #    "total_kokoroPatients": total_patientProfiles,
        #    "nation_distribution": json.dumps(nation_distribution),
        #    "sex_distribution": json.dumps(sex_distribution),
        #    "dob_distribution": json.dumps(dob_distribution),
        #    "sex_kokoroDistribution": json.dumps(sexProfiles_distribution),
        #})

        ### NEW ###
        context.update({
            "total_kokoroPatients": total_patientProfiles,
            #"total_procedures": total_procedures,
            "sex_kokoroDistribution": json.dumps(sexProfiles_distribution),
            "nation_distribution": json.dumps(nationProfiles_distribution),
            "dob_distribution": json.dumps(dob_distribution),
        })

        return context

class AboutPageView(TemplateView):
    template_name = "about.html"