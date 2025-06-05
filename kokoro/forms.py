from django import forms
from .models import PatientProfile

class PatientProfileForm(forms.ModelForm):

	cardioref_id = forms.CharField(
		required=False,
		error_messages={'invalid': 'Cardioref ID must be a number.',}
	)

	class Meta:
		model = PatientProfile
		fields = '__all__'

	def clean_cardioref_id(self):
		value = self.cleaned_data['cardioref_id']
		if value in (None, ''):
			return None
		try:
			value = int(value)
		except ValueError:
			raise forms.ValidationError("Cardioref ID must be a number.")
		if value < 0:
			raise forms.ValidationError("Cardioref ID must be a positive integer.")
		return value