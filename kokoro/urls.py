from django.urls import path
from .views import KokoroHome

urlpatterns = [
	path("", KokoroHome.as_view(), name="kokoro"),
]