from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Count
from collections import Counter
import json
from patients.models import Patient, Sample, Analysis
from kokoro.models import PatientProfile

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
        total_PatientProfile = PatientProfile.objects.count()
        total_patients = Patient.objects.count()
        total_samples = Sample.objects.count()
        total_analysis = Analysis.objects.count()

        # Get distribution data
        nations = Patient.objects.values_list("nation", flat=True)
        sex_counts = Patient.objects.values_list("sex", flat=True)
        dob_years = Patient.objects.values_list("date_of_birth", flat=True)

        # Process distributions
        nation_distribution = dict(Counter(nations))
        sex_distribution = dict(Counter(sex_counts))
        dob_distribution = dict(Counter(d.year for d in dob_years if d))  # Group by birth year

        # Add data to context
        context.update({
            "total_patients": total_patients,
            "total_samples": total_samples,
            "total_analysis": total_analysis,
            "nation_distribution": json.dumps(nation_distribution),
            "sex_distribution": json.dumps(sex_distribution),
            "dob_distribution": json.dumps(dob_distribution),
            "total_PatientProfile": total_PatientProfile,
        })

        return context

class AboutPageView(TemplateView):
	template_name = "about.html"