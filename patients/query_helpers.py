# patients/query_helpers.py
from .models import Patient, Sample, Analysis
from .filters import DemographicFilter, SampleFilter, AnalysisFilter

def get_filtered_patients(request):
    """
    Returns a queryset of Patients filtered based on the combined criteria:
    - Demographic filters on the Patient model.
    - Sample filters on the Sample model (with key 'sample_type').
    - Analysis filters on the Analysis model (with key 'analysis_type').

    For a patient to be included, there must exist at least one sample that satisfies
    both the sample and analysis filter criteria.
    """
    # Start with all patients.
    patient_qs = Patient.objects.all().distinct()

    # Apply demographic filters.
    demo_filter = DemographicFilter(request.GET, queryset=patient_qs)
    patient_qs = demo_filter.qs

    # Prepare the sample and analysis filters.
    sample_filter_obj = SampleFilter(request.GET, queryset=Sample.objects.all())
    analysis_filter_obj = AnalysisFilter(request.GET, queryset=Analysis.objects.all())

    # Get the filtered querysets from the filter objects.
    sample_qs = sample_filter_obj.qs
    analysis_qs = analysis_filter_obj.qs

    # Explicitly check if the GET parameter for sample_type is valid.
    sample_type_val = request.GET.get("sample_type")
    if sample_type_val:
        distinct_sample_types = list(Sample.objects.values_list("type", flat=True).distinct())
        if sample_type_val not in distinct_sample_types:
            sample_qs = Sample.objects.none()

    # Similarly, check analysis_type.
    analysis_type_val = request.GET.get("analysis_type")
    if analysis_type_val:
        distinct_analysis_types = list(Analysis.objects.values_list("type", flat=True).distinct())
        if analysis_type_val not in distinct_analysis_types:
            analysis_qs = Analysis.objects.none()

    # Determine if either sample or analysis filters are active.
    sample_filter_active = any(request.GET.get(field) for field in sample_filter_obj.form.fields)
    analysis_filter_active = any(request.GET.get(field) for field in analysis_filter_obj.form.fields)

    if sample_filter_active or analysis_filter_active:
        # Start with all samples.
        combined_sample_qs = Sample.objects.all()
        if sample_filter_active:
            combined_sample_qs = sample_qs
        if analysis_filter_active:
            combined_sample_qs = combined_sample_qs.filter(analyses__in=analysis_qs).distinct()
        # Filter patients to those having at least one qualifying sample.
        patient_qs = patient_qs.filter(samples__in=combined_sample_qs).distinct()

    return patient_qs
