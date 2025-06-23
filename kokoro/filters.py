import django_filters
from .models import PatientProfile
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
    sex = django_filters.ChoiceFilter(choices=PatientProfile.Sex.choices, label="Sex")
    # nationality: filtro personalizzato con method="filter_nationality" → definito più sotto.
    nationality = django_filters.ChoiceFilter(label="Nationality", method="filter_nationality")

    #Sovrascrive il costruttore __init__ per costruire dinamicamente la lista di nazionalità presenti nel database:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct nation values from the Patient records (ignoring empty ones).
        # exclude(nation=""): ignora i record con campo vuoto.
        distinct_nations = PatientProfile.objects.exclude(nation="").values_list("nation", flat=True).distinct()
        # Build choices list: include a blank choice for no selection.
        # values_list(..., flat=True).distinct(): ottiene una lista dei valori univoci del campo nation.
        # [("", "---------")] + [...]: aggiunge una scelta vuota (per non selezionare nulla).
        choices = [("", "---------")] + [(nation, nation) for nation in distinct_nations]
        # Aggiorna le scelte del filtro nationality dinamicamente, sia in .extra che in .field.
        self.filters["nationality"].extra["choices"] = choices
        self.filters["nationality"].field.choices = choices

    # Metodo associato al filtro nationality.
    def filter_nationality(self, qs, name, value):
        if value:
               # Filtra per nation=value solo se il valore non è vuoto.
            return qs.filter(nation=value)
        # Altrimenti ritorna l'intero queryset (nessun filtro applicato).
        return qs

    class Meta:
        model = PatientProfile
        fields = ["sex", "nationality"]