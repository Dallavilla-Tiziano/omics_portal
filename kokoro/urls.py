from django.urls import path
from .views import KokoroHome, TherapyAutocomplete, AllergyAutocomplete, StudyAutocomplete

urlpatterns = [
	path("", KokoroHome.as_view(), name="kokoro"),
    path('therapy-autocomplete/', TherapyAutocomplete.as_view(), name='therapy-autocomplete'),
    path('allergy-autocomplete/', AllergyAutocomplete.as_view(), name='allergy-autocomplete'),
    path('study-autocomplete/', StudyAutocomplete.as_view(), name='study-autocomplete'),
]