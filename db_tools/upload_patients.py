from patients.models import Patient
import pandas as pd

patients = pd.read_csv('/code/db_tools/clinical_imtc_ef_merged.csv')

for index, row in patients.iterrows():
	if pd.isna(row['fin']):
		fin_value = None
	else:
		fin_value = row['fin']

	if pd.isna(row['family_status']):
		family_status_value = ''
	else:
		family_status_value = row['family_status']

	patient = Patient(
	last_name = row['last_name'],
	first_name = row['first_name'],
	sex = row['sex'],
	date_of_birth = row['birth_date'],
	nation = row['nation'],
	region = row['region'],
	province = row['province'],
	cardioref_id = row['id_cardioref'],
	patient_type = family_status_value,
	fin = fin_value
	)
	print(patient)
	patient.save()