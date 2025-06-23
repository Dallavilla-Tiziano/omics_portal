# patients/query_helpers.py
from .models import PatientProfile
from .filters import DemographicFilter

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
    patient_qs = PatientProfile.objects.all().distinct()

    # Apply demographic filters.
    demo_filter = DemographicFilter(request.GET, queryset=patient_qs)
    patient_qs = demo_filter.qs

    return patient_qs
