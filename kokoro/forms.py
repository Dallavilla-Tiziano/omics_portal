from django import forms
from .models import (PatientProfile, Late_potentials, Study, Ablation, Adrenaline_test)
from .validators import (validate_not_in_future, clean_positive_float, clean_start_end_date, clean_positive_int)

class AdrenalineTestForm(forms.ModelForm):

	adrenaline_dose = forms.CharField(required=False)

	class Meta:
		model = Adrenaline_test
		fields = '__all__'

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	def clean_adrenaline_dose(self):
		return clean_positive_float(self.cleaned_data.get('adrenaline_dose'), label="Adrenaline Dose")


class AblationForm(forms.ModelForm):

	class Meta:
		model = Ablation
		fields = '__all__'

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

class PatientProfileForm(forms.ModelForm):

	cardioref_id = forms.CharField(required=False)

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
		return validate_not_in_future(self.cleaned_data.get('date_of_exam'))

class StudyForm(forms.ModelForm):

	def clean(self):
		cleaned_data = super().clean()
		start = cleaned_data.get('start_date')
		end = cleaned_data.get('end_date')
		clean_start_end_date(start, end)
		return cleaned_data

	class Meta:
		model = Study
		fields = '__all__'