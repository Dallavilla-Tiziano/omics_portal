from django.urls import path
from .views import KokoroHomeView

urlpatterns = [
	path("", KokoroHomeView.as_view(), name="kokoro_patient_list"),
]