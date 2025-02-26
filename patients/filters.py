import django_filters
from dal import autocomplete
from .models import Patient

class PatientFilter(django_filters.FilterSet):
    sex = django_filters.ChoiceFilter(choices=[("M", "Male"), ("F", "Female")], label="Sex")
    patient_type = django_filters.ChoiceFilter(choices=[("P", "Proband"), ("R", "Relative")], label="Status")
    nation = django_filters.ChoiceFilter(
        field_name="nation",
        choices=[(c, c) for c in Patient.objects.values_list('nation', flat=True).distinct()],
        label="Nation",
        lookup_expr="icontains"  # Allows partial matches when typing
    )

    class Meta:
        model = Patient
        fields = ["sex", "patient_type", "nation"]
