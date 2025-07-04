import django_filters
from .models import PatientProfile
from django.db.models import Q
from django.contrib.auth import get_user_model

# Salviamo il modello utente in una variabile chiamata User, 
# così possiamo usarlo in seguito nei filtri (es. ModelChoiceFilter).
User = get_user_model()

# Eredita da ChoiceFilter e la modifica: serve a evitare filtraggi invalidi.
class StrictChoiceFilter(django_filters.ChoiceFilter):
    # qs: è il queryset da filtrare.
    # # value: è il valore scelto dall'utente.
    def filter(self, qs, value):
        # Use the field's choices, which should be a list of tuples.
        valid_choices = dict(self.field.choices)
        # Se il valore passato non è presente tra le scelte valide, restituisce un queryset vuoto (qs.none()).
        if value not in valid_choices:
            return qs.none()
        # Altrimenti, chiama il metodo .filter() originale della superclasse.
        return super().filter(qs, value)

# Inizia una classe FilterSet, ovvero una collezione di filtri applicabili a un modello: in questo caso, il modello è Patient Profile.
class DemographicFilter(django_filters.FilterSet):
    """ Filters for patient demographics """
    search = django_filters.CharFilter(method="filter_search", label="Search")
    sex = django_filters.ChoiceFilter(choices=PatientProfile.Sex.choices, label="Sex")
    nationality = django_filters.ChoiceFilter(label="Nation", method="filter_nationality")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate nationality choices
        distinct_nations = PatientProfile.objects.exclude(nation="").values_list("nation", flat=True).distinct()
        choices = [("", "---------")] + [(nation, nation) for nation in distinct_nations]
        self.filters["nationality"].extra["choices"] = choices
        self.filters["nationality"].field.choices = choices

    def filter_nationality(self, qs, name, value):
        if value:
            return qs.filter(nation=value)
        return qs

    def filter_search(self, qs, name, value):
        if value:
            return qs.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(cardioref_id__icontains=value)
            )
        return qs

    class Meta:
        model = PatientProfile
        fields = ["sex", "nationality", "search"]