from dal import autocomplete
from django.views.generic import TemplateView
from .models import Therapy, Study, PatientProfile
from django.db.models import Q

class KokoroHome(TemplateView):
	template_name = "kokoro/kokoro.html"

class TherapyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Therapy.objects.all()
		# Support both 'q' and 'term' (DAL uses 'q', but Select2 might use 'term')
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(name__icontains=search)
		return qs

class AllergyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Therapy.objects.all()
		# Support both 'q' and 'term' (DAL uses 'q', but Select2 might use 'term')
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(name__icontains=search)
		return qs

class StudyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Study.objects.all()
		# Support both 'q' and 'term' (DAL uses 'q', but Select2 might use 'term')
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(name__icontains=search)
		return qs

class PatientProfileAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = PatientProfile.objects.all()
		search = self.q or self.request.GET.get('term')
		if search:
			qs = qs.filter(
				Q(last_name__icontains=search) |
				Q(first_name__icontains=search) |
				Q(cardioref_id__icontains=search)
			)
		return qs