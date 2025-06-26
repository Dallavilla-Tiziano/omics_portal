from django import forms
from .models import (PatientProfile, Late_potentials, Study,
						Ablation, Adrenaline_test, Ajmaline_test,
						Clinical_evaluation, ClinicalEvent, CoronaryIntervention,
						DeviceEvent, DeviceImplant, DeviceInstance,
						EP_study, ECG, ECHO,
						Flecainide_test, Genetic_profile, Genetic_status,
						Genetic_test, RMN_TC_PH, Sample, ValveIntervention
					)
from .validators import (validate_not_in_future, clean_positive_float, clean_start_end_date,
							clean_positive_int
						)
from dal import autocomplete
from django.forms.widgets import DateInput


class ValveInterventionForm(forms.ModelForm):

	def clean_date(self):
		return validate_not_in_future(self.cleaned_data.get('date'))

	class Meta:
		model = ValveIntervention
		fields = '__all__'

class SampleForm(forms.ModelForm):

	collection_date = forms.DateField()

	pbmc_vials_n = forms.CharField(required=False)
	pellet_vials_n = forms.CharField(required=False)
	rna_vials_n = forms.CharField(required=False)
	plasma_cold_vials_n = forms.CharField(required=False)
	plasma_ambient_vials_n = forms.CharField(required=False)
	rin = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive integer
		int_fields = [
			('pbmc_vials_n', 'Number of PBMC Vials'),
			('pellet_vials_n', 'Number of Pellet Vials'),
			('rna_vials_n', 'Number of RNA Vials'),
			('plasma_cold_vials_n', 'Number of Plasma Vials (4°C)'),
			('plasma_ambient_vials_n', 'Number of Plasma Vials (Room Temperature)'),
			('rin', 'RNA Integrity Number'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)
		return cleaned_data

	def clean_collection_date(self):
		return validate_not_in_future(self.cleaned_data.get('collection_date'))

	class Meta:
		model = Sample
		fields = '__all__'


class RMN_TC_PHTest(forms.ModelForm):

	def clean_date_of_exam(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_exam'))

	class Meta:
		model = RMN_TC_PH
		fields = '__all__'

class Genetic_testForm(forms.ModelForm):

	Consent_date = forms.DateField()
	report_data = forms.DateField()
	aliquota = forms.CharField(required=False)
	
	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive integer
		int_fields = [
			('aliquota', 'Number of Aliquotes'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)
		return cleaned_data

	def clean_Consent_date(self):
		return validate_not_in_future(self.cleaned_data.get('Consent_date'))

	def clean_report_data(self):
		return validate_not_in_future(self.cleaned_data.get('report_data'))

	class Meta:
		model = Genetic_test
		fields = '__all__'

class Genetic_statusForm(forms.ModelForm):

	family_members = forms.CharField(required=False)
	children = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive integer
		int_fields = [
			('family_members', 'Number of Family Members'),
			('children', 'Number of Childrens'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)
		return cleaned_data

	class Meta:
		model = Genetic_status
		fields = '__all__'

class Genetic_profileForm(forms.ModelForm):

	FIN_progressive_genetics = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive integer
		int_fields = [
			('FIN_progressive_genetics', 'Family Identification Number (FIN)'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)
		return cleaned_data

	class Meta:
		model = Genetic_profile
		fields = '__all__'		

class Flecainide_testForm(forms.ModelForm):

	flecainide_dose = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('flecainide_dose', 'Flecainide Dose'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data	

	def clean_date_of_provocative_test(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_provocative_test'))

	class Meta:
		model = Flecainide_test
		fields = '__all__'

class ECHOForm(forms.ModelForm):

	max_pressure = forms.CharField(required=False)	
	min_pressure = forms.CharField(required=False)
	lvef = forms.CharField(required=False)
	tapse = forms.CharField(required=False)
	left_atrial_area = forms.CharField(required=False)
	la_diameter = forms.CharField(required=False)
	la_end_diastolic_volume = forms.CharField(required=False)
	la_end_systolic_volume = forms.CharField(required=False)
	lv_end_diastolic_volume = forms.CharField(required=False)
	lv_end_systolic_volume = forms.CharField(required=False)
	lv_end_diastolic_diameter = forms.CharField(required=False)
	lv_end_systolic_diameter = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('max_pressure', 'Max Pressure'),
			('min_pressure', 'Min Pressure'),
			('hr', 'hr'),
			('rr', 'rr'),
			('pq', 'pq'),
			('pr', 'pr'),
			('qrs', 'qrs'),
			('qt', 'qt'),
			('qtc', 'qtc'),
			('max_st', 'max st'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data

	def clean_date_of_exam(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_exam'))

	class Meta:
		model = ECHO
		fields = '__all__'

class ECGForm(forms.ModelForm):

	max_pressure = forms.CharField(required=False)	
	min_pressure = forms.CharField(required=False)
	hr = forms.CharField(required=False)
	rr = forms.CharField(required=False)
	pq = forms.CharField(required=False)
	pr = forms.CharField(required=False)
	qrs = forms.CharField(required=False)
	qt = forms.CharField(required=False)
	qtc = forms.CharField(required=False)
	max_st = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('max_pressure', 'Max Pressure'),
			('min_pressure', 'Min Pressure'),
			('hr', 'hr'),
			('rr', 'rr'),
			('pq', 'pq'),
			('pr', 'pr'),
			('qrs', 'qrs'),
			('qt', 'qt'),
			('qtc', 'qtc'),
			('max_st', 'max st'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data

	def clean_date_of_exam(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_exam'))

	class Meta:
		model = ECG
		fields = '__all__'

class EP_studyForm(forms.ModelForm):

	total_area = forms.CharField(required=False)
	bas_area_a_160 = forms.CharField(required=False)

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('total_area', 'Total Area'),
			('bas_area_a_160', 'Basal Area Above 160'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)
		return cleaned_data

	def clean_date_of_provocative_test(self):
		return validate_not_in_future(self.cleaned_data.get('date_of_provocative_test'))

	class Meta:
		model = EP_study
		fields = '__all__'

class DeviceInstanceForm(forms.ModelForm):

	class Meta:
		model = DeviceInstance
		fields = '__all__'

class DeviceImplantForm(forms.ModelForm):

	lv4_ring = forms.CharField(required=False)
	lv3_ring = forms.CharField(required=False)
	lv2_ring = forms.CharField(required=False)
	lv1_tip = forms.CharField(required=False)
	v1 =  forms.CharField(required=False)
	lv_pulse_configuration_2_lv2 = forms.CharField(required=False)
	pacing_impendance1 = forms.CharField(required=False)
	v2 =  forms.CharField(required=False)
	pacing_impendance2 = forms.CharField(required=False)
	v3 =  forms.CharField(required=False)
	pacing_impendance3 = forms.CharField(required=False)

	ms1 = forms.CharField(required=False)
	ms2 = forms.CharField(required=False)
	ms3 = forms.CharField(required=False)	

	def clean(self):
		cleaned_data = super().clean()
		# Fields that should be validated as positive floats
		float_fields = [
			('lv4_ring', 'lv4 ring'),
			('lv3_ring', 'lv3 ring'),
			('lv2_ring', 'lv2 ring'),
			('lv1_tip', 'lv1 tip'),
			('v1', 'v1'),
			('lv_pulse_configuration_2_lv2', 'lv pulse configuration 2 lv2'),
			('pacing_impendance1', 'pacing impendance 1'),
			('v2', 'v2'),
			('pacing_impendance2', 'pacing impendance 2'),
			('v3', 'v3'),
			('pacing_impendance3', 'pacing impendance 3'),
		]

		for field, label in float_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_float(value, label=label)

		int_fields = [
			('ms1', 'ms1'),
			('ms2', 'ms2'),
			('ms3', 'ms3'),
		]

		for field, label in int_fields:
			value = cleaned_data.get(field)
			cleaned_data[field] = clean_positive_int(value, label=label)

		return cleaned_data

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
		widgets = {
			'patient': autocomplete.ModelSelect2(
				url='patientprofile-autocomplete'
			),
			'date_of_exam': DateInput(attrs={'type': 'date'})
		}

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
		widgets = {
			'start_date': DateInput(attrs={'type': 'date'}),
			'end_date': DateInput(attrs={'type': 'date'}),
		}