from django import forms
from .models import (PatientProfile, Late_potentials, Study,
						Ablation, Adrenaline_test, Ajmaline_test,
						Clinical_evaluation, ClinicalEvent, CoronaryIntervention,
						DeviceEvent, DeviceImplant, 
					)
from .validators import (validate_not_in_future, clean_positive_float, clean_start_end_date,
							clean_positive_int
						)
from dal import autocomplete

class DeviceImplantForm(forms.ModelForm):

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = DeviceImplant
		fields = '__all__'

class DeviceEventForm(forms.ModelForm):

	n_icd_shock_appropriate_pre_rf = forms.CharField(required=False)
	n_icd_shock_inappropriate_pre_rf = forms.CharField(required=False)
	n_icd_shock_appropriate_post_brs_diagnosis = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive integer
		int_fields = [
			('n_icd_shock_appropriate_pre_rf', 'Number of appropriate icd shock pre rf'),
			('n_icd_shock_inappropriate_pre_rf', 'Number of inappropriate icd shock pre rf'),
			('n_icd_shock_appropriate_post_brs_diagnosis', 'Number of appropriate icd shock post brs diagnosis'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)
		return cleaned_data

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = DeviceEvent
		fields = '__all__'

class CoronaryInterventionForm(forms.ModelForm):

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = CoronaryIntervention
		fields = '__all__'

class ClinicalEventForm(forms.ModelForm):

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = ClinicalEvent
		fields = '__all__'

class Clinical_evaluationForm(forms.ModelForm):

	def clean_date_of_visit(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_visit'))

	class Meta:
		model = Clinical_evaluation
		fields = '__all__'

class AjmalineTestForm(forms.ModelForm):

	ajmaline_dose = forms.CharField(required=False)
	ajmaline_dose_per_kg = forms.CharField(required=False)	
	bas_area_a_160 = forms.CharField(required=False)
	bas_area_a_180 = forms.CharField(required=False)
	bas_area_a_200 = forms.CharField(required=False)
	bas_area_a_250 = forms.CharField(required=False)
	bas_area_a_280_300 = forms.CharField(required=False)
	pdm = forms.CharField(required=False)
	dose_to_positive_ecg = forms.CharField(required=False)	

	def clean_date_of_provocative_test(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_provocative_test'))

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('ajmaline_dose', 'Ajmaline Dose'),
			('ajmaline_dose_per_kg', 'Ajmaline Dose per Kg'),
			('bas_area_a_160', 'Basal Area A160'),
			('bas_area_a_180', 'Basal Area A180'),
			('bas_area_a_200', 'Basal Area A200'),
			('bas_area_a_250', 'Basal Area A250'),
			('bas_area_a_280_300', 'Basal Area A280-A300'),
			('pdm', 'PDM'),
			('dose_to_positive_ecg', 'Dose to Positive ECG'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data

	class Meta:
		model = Ajmaline_test
		fields = '__all__'

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
	
	total_area = forms.CharField(required=False)
	bas_area_a_160 = forms.CharField(required=False)
	bas_area_a_180 = forms.CharField(required=False)
	bas_area_a_200 = forms.CharField(required=False)
	basal_pdm = forms.CharField(required=False)
	total_rf_time = forms.CharField(required=False)
	rf_w = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('total_area', 'Total Area'),
			('bas_area_a_160', 'Basal Area A160'),
			('bas_area_a_180', 'Basal Area A180'),
			('bas_area_a_200', 'Basal Area A200'),
			('basal_pdm', 'Basal PDM'),
			('total_rf_time', 'Total RF Time'),
			('rf_w', 'RF W'),
		]
		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = Ablation
		fields = '__all__'

class PatientProfileForm(forms.ModelForm):

	cardioref_id = forms.CharField(required=False)

	class Meta:
		model = PatientProfile
		fields = '__all__'
		widgets = {
			'therapies': autocomplete.ModelSelect2Multiple(
				url='therapy-autocomplete'
			),
			'allergies': autocomplete.ModelSelect2Multiple(
				url='allergy-autocomplete'
			),
			'studies': autocomplete.ModelSelect2Multiple(
				url='study-autocomplete'
			),
		}

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