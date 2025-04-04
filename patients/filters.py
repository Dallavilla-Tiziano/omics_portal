import django_filters
from .models import Patient, Sample, Analysis
from django.contrib.auth import get_user_model

User = get_user_model()

class StrictChoiceFilter(django_filters.ChoiceFilter):
    def filter(self, qs, value):
        # Use the field's choices, which should be a list of tuples.
        valid_choices = dict(self.field.choices)
        if value not in valid_choices:
            return qs.none()
        return super().filter(qs, value)

class DemographicFilter(django_filters.FilterSet):
    """ Filters for patient demographics """
    sex = django_filters.ChoiceFilter(choices=Patient.Sex.choices, label="Sex")
    patient_type = django_filters.ChoiceFilter(choices=Patient.Patient_type.choices, label="Patient Type")
    nationality = django_filters.ChoiceFilter(label="Nationality", method="filter_nationality")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct nation values from the Patient records (ignoring empty ones).
        distinct_nations = Patient.objects.exclude(nation="").values_list("nation", flat=True).distinct()
        # Build choices list: include a blank choice for no selection.
        choices = [("", "---------")] + [(nation, nation) for nation in distinct_nations]
        self.filters["nationality"].extra["choices"] = choices
        self.filters["nationality"].field.choices = choices

    def filter_nationality(self, qs, name, value):
        if value:
            return qs.filter(nation=value)
        return qs

    class Meta:
        model = Patient
        fields = ["sex", "patient_type", "nationality"]

class SampleFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Sample.SampleStatus.choices, 
        label="Sample Status"
    )
    sample_type = django_filters.ChoiceFilter(
        field_name="type",
        label="Sample Type",
        method="filter_sample_type",
        choices=[]  # initially empty, will be set in __init__
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct sample types from the database.
        distinct_types = list(Sample.objects.values_list("type", flat=True).distinct())
        choices = [(t, t) for t in distinct_types]
        # Update the filter's choices in both the extra and the field.
        self.filters["sample_type"].extra["choices"] = choices
        self.filters["sample_type"].field.choices = choices

    def filter_sample_type(self, qs, name, value):
        if value not in dict(self.filters["sample_type"].field.choices):
            return qs.none()
        return qs.filter(**{name: value})

    class Meta:
        model = Sample
        fields = ["sample_type", "status"]

class AnalysisFilter(django_filters.FilterSet):
    analysis_type = django_filters.ChoiceFilter(
        field_name="type",
        label="Analysis Type",
        method="filter_analysis_type",
        choices=[]  # initially empty, will be set in __init__
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct analysis types from the database.
        distinct_types = list(Analysis.objects.values_list("type", flat=True).distinct())
        choices = [(t, t) for t in distinct_types]
        self.filters["analysis_type"].extra["choices"] = choices
        self.filters["analysis_type"].field.choices = choices

    def filter_analysis_type(self, qs, name, value):
        if value not in dict(self.filters["analysis_type"].field.choices):
            return qs.none()
        return qs.filter(**{name: value})

    performed_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(analysis__isnull=False).distinct(),
        field_name="performed_by",
        label="Performed By"
    )

    class Meta:
        model = Analysis
        fields = ["analysis_type", "performed_by"]