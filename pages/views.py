from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Count
from django.db.models.functions import ExtractYear
from collections import Counter
import json
from datetime import date
from kokoro.models import (
    PatientProfile, Ajmaline_test, EP_study, Flecainide_test, Adrenaline_test,
    Ablation, DeviceImplant, Genetic_test, ECG, ECHO, RMN_TC_PH, ResearchAnalysis,
    ValveIntervention, CoronaryIntervention, Genetic_sample
)


class HomePageView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        patients = PatientProfile.objects.all()

        # <!-- 1ST SECTION: All our patients -->
        # Average age
        ages = [(today - p.date_of_birth).days // 365 for p in patients if p.date_of_birth]
        avg_age = round(sum(ages) / len(ages), 1) if ages else 0
        # Sex distribution
        sex_counts = patients.values_list("sex", flat=True)
        sex_distribution = dict(Counter(sex_counts))
        # Age distribution
        age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        age_labels = [f"{age_bins[i]}–{age_bins[i+1]-1}" for i in range(len(age_bins)-1)]
        age_distribution = dict.fromkeys(age_labels, 0)
        for age in ages:
            for i in range(len(age_bins) - 1):
                if age_bins[i] <= age < age_bins[i + 1]:
                    age_distribution[age_labels[i]] += 1
                    break

        # <!-- PROCEDURE SECTION -->
        # Procedure count
        procedures_data = {
            'Ablation': Ablation.objects.count(),
            'Device Implant': DeviceImplant.objects.count(),
            'Valve Intervention': ValveIntervention.objects.count(),
            'Coronary Intervention': CoronaryIntervention.objects.count(),
        }
        # Procedures by year
        def get_by_year(model):
            return {
                str(entry['year']): entry['count']
                for entry in model.objects.filter(date__year__gte=2000)
                    .annotate(year=ExtractYear('date'))
                    .values('year')
                    .annotate(count=Count('id'))
                    .order_by('year')
            }
        ablation_by_year = get_by_year(Ablation)
        device_by_year = get_by_year(DeviceImplant)
        valve_by_year = get_by_year(ValveIntervention)
        coronary_by_year = get_by_year(CoronaryIntervention)

        # <!-- GENETICS -->
        common_mutations = (
            Genetic_test.objects.values('var_p__name')
            .exclude(var_p__name__isnull=True)
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        patients_with_mutation = Genetic_test.objects.exclude(var_p=None).values('patient').distinct().count()
        test_distribution = (
            Genetic_test.objects.values('testType')
            .annotate(count=Count('id'))
        )
        # Most common mutations (on var_p)
        common_mutations = (
            Genetic_test.objects.values('var_p__name')
            .exclude(var_p__name__isnull=True)
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        # Number of patients with known mutation
        patients_with_mutation = Genetic_test.objects.exclude(var_p=None).values('patient').distinct().count()
        # Test type distribution
        test_distribution = (
            Genetic_test.objects.values('testType')
            .annotate(count=Count('id'))
        )
        # Genetic Samples trend by year
        samples_by_year = {
            str(entry['year']): entry['count']
            for entry in Genetic_sample.objects.filter(blood_sample_date__year__gte=2000)
            .annotate(year=ExtractYear('blood_sample_date'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        }

        context.update({
            # PATIENTS
            "total_patients": patients.count(),
            "avg_age": avg_age,
            "n_male": patients.filter(sex="M").count(),
            "n_female": patients.filter(sex="F").count(),
            "sex_distribution": json.dumps(sex_distribution),
            "age_distribution": json.dumps(age_distribution),
            "n_enrolled": patients.filter(studies__isnull=False).distinct().count(),

            # PROVOCATIVE TESTS 
            # Ajmaline test
            "n_ajmaline": Ajmaline_test.objects.count(),
            "n_aj_pos": Ajmaline_test.objects.filter(ajmaline_result="Positive").count(),
            "n_aj_neg": Ajmaline_test.objects.filter(ajmaline_result="Negative").count(),
            "n_aj_sosp": Ajmaline_test.objects.filter(ajmaline_result="Weakly positive").count(),
            # EP Study
            "n_ep": EP_study.objects.count(),
            "n_ep_pos": EP_study.objects.filter(ep_result="Positive").count(),
            "n_ep_neg": EP_study.objects.filter(ep_result="Negative").count(),
            # Flecainide
            "n_flec": Flecainide_test.objects.count(),
            "n_flec_pos": Flecainide_test.objects.filter(flecainide_result="Positive").count(),
            "n_flec_neg": Flecainide_test.objects.filter(flecainide_result="Negative").count(),
            # Adrenaline
            "n_adr": Adrenaline_test.objects.count(),
            "n_adr_pos": Adrenaline_test.objects.filter(adrenaline_result="Positive").count(),
            "n_adr_neg": Adrenaline_test.objects.filter(adrenaline_result="Negative").count(),
            "n_adr_sosp": Adrenaline_test.objects.filter(adrenaline_result="Weakly positive").count(),

            # PROCEDURES
            "n_ablation": procedures_data["Ablation"],
            "n_devices": procedures_data["Device Implant"],
            "n_valve": procedures_data["Valve Intervention"],
            "n_coro": procedures_data["Coronary Intervention"],
            "procedures_data": json.dumps(procedures_data),
            "ablation_by_year": json.dumps(ablation_by_year),
            "device_by_year": json.dumps(device_by_year),
            "valve_by_year": json.dumps(valve_by_year),
            "coronary_by_year": json.dumps(coronary_by_year),

            # GENETICS
            "n_genetic": Genetic_test.objects.count(),
            "n_ngs": Genetic_test.objects.filter(testType="NGS").count(),
            "n_mutuna": Genetic_test.objects.filter(testType="Mutuna").count(),
            "common_mutations": common_mutations,
            "n_patients_with_mutation": patients_with_mutation,
            "test_distribution": json.dumps({entry['testType']: entry['count'] for entry in test_distribution}),
            "total_Samples": 0,
            "total_researchAnalysis": ResearchAnalysis.objects.count(),
            "common_mutations": common_mutations,
            "n_patients_with_mutation": patients_with_mutation,
            "test_distribution": json.dumps({entry['testType']: entry['count'] for entry in test_distribution}),
            "total_samples": Genetic_sample.objects.count(),
            "sample_by_year": json.dumps(samples_by_year),
        })

        return context


class AboutPageView(TemplateView):
    template_name = "about.html"