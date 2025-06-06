from django import forms
from .models import (PatientProfile, Late_potentials)
from .validators import (validate_not_in_future, clean_positive_float)

class PatientProfileForm(forms.ModelForm):

	cardioref_id = forms.CharField(
		required=False,
		error_messages={'invalid': 'Cardioref ID must be a number.',}
	)

	class Meta:
		model = PatientProfile
		fields = '__all__'

	def clean_cardioref_id(self):
		return clean_positive_int(self.cleaned_data.get('cardioref_id'), label="Cardioref id") 

	def clean_date_of_birth(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_birth'))
		


class LatePotentialForm(forms.ModelForm):
	basal_lp1 = forms.CharField(required=False)
	basal_lp2 = forms.CharField(required=False)
	basal_lp3 = forms.CharField(required=False)
	basal_lp4 = forms.CharField(required=False)

	class Meta:
		model = Late_potentials
		fields = '__all__'

	def clean_basal_lp1(self):
		return clean_positive_float(self.cleaned_data.get('basal_lp1'), label="Basal LP1")

	def clean_basal_lp2(self):
		return clean_positive_float(self.cleaned_data.get('basal_lp2'), label="Basal LP2")

	def clean_basal_lp3(self):
		return clean_positive_float(self.cleaned_data.get('basal_lp3'), label="Basal LP3")

	def clean_basal_lp4(self):
		return clean_positive_float(self.cleaned_data.get('basal_lp4'), label="Basal LP4")

	def clean_date_of_exam(self):
		doe = self.cleaned_data.get('date_of_exam')
		validate_not_in_future(doe)
		return doe