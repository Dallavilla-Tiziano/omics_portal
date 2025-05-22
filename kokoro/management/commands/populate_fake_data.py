from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from kokoro.models import (
	PatientProfile, Study, Therapy, Gene, Mutation, Doctors,
	Sample, ResearchAnalysis, Ablation, DeviceImplant, ValveIntervention,
	CoronaryIntervention, ECG, ECHO, RMN_TC_PH, Late_potentials,
	Clinical_evaluation, ClinicalEvent, Genetic_profile, Genetic_status,
	Genetic_sample, Genetic_test, DeviceType, DeviceInstance, DeviceEvent, PatientStudy, Symptoms, Cardiomiopathies, Riskfactors, Comorbidities, EP_study, Flecainide_test, Adrenaline_test, Ajmaline_test
)

fake = Faker()

class Command(BaseCommand):
	help = "Populate database with realistic fake data for testing"
	
	def create_device_types(self):
		seeds = [
			{
				"type":    DeviceType.Type.PACE_MAKER,
				"company": DeviceType.Company.MEDTRONIC,
				"model":   DeviceType.Model.IN7F4IS4,
				"design":  DeviceType.Design.SD_PACEMAKER,
			},
			{
				"type":    DeviceType.Type.LOOP_RECORDER,
				"company": DeviceType.Company.BIOTRONIK,
				"model":   DeviceType.Model.RI7HFQP,
				"design":  DeviceType.Design.SD_CHAMBER_ICD,
			},
		]
		for data in seeds:
			DeviceType.objects.get_or_create(
				type    = data["type"],
				defaults={
					"company": data["company"],
					"model":   data["model"],
					"design":  data["design"],
				},
			)
		self.stdout.write(self.style.SUCCESS("✅ Seeded DeviceType table."))

	def create_device_records(self, patients, count):
		"""
		Create DeviceInstance + DeviceImplant for each record.
		"""
		device_types = list(DeviceType.objects.all())
		if not device_types:
			raise CommandError("No DeviceType available—run create_device_types first.")
		for _ in range(count):
			patient = random.choice(patients)
			# pick a device type
			dt = random.choice(device_types)
			# create the instance
			device = DeviceInstance.objects.create(
				device_type   = dt,
				serial_number = fake.uuid4(),
				patient       = patient,
			)
			# create the implant linked to that instance
			DeviceImplant.objects.create(
				device_instance = device,
				patient         = patient,
				date            = fake.date_between(
									 start_date=patient.date_of_birth + relativedelta(years=18),
									 end_date='today'
								 ),
				lv4_ring        = random.uniform(20,50),
				lv3_ring        = random.uniform(20,50),
				lv2_ring        = random.uniform(20,50),
				lv1_tip         = random.uniform(20,50),
				v1              = random.uniform(0.1,5.0),
				ms1             = random.randint(0,10),
				lv_pulse_configuration_2_lv2 = random.uniform(20,50),
				pacing_impendance1           = random.uniform(300,1000),
				v2              = random.uniform(0.1,5.0),
				ms2             = random.randint(0,10),
				pacing_impendance2           = random.uniform(300,1000),
				v3              = random.uniform(0.1,5.0),
				ms3             = random.randint(0,10),
				pacing_impendance3           = random.uniform(300,1000),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} device records."))

	def create_symptoms(self):
		"""
		Seed the Symptoms lookup table.
		"""
		names = ["Chest pain", "Dyspnea", "Palpitations", "Fatigue", "Syncope"]
		for name in names:
			Symptoms.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(names)} Symptoms."))

	def create_cardiomiopathies(self):
		"""
		Seed the Cardiomiopathies lookup table.
		"""
		names = [
			"Dilated", "Hypertrophic", "Restrictive",
			"Arrhythmogenic RV", "Ischemic"
		]
		for name in names:
			Cardiomiopathies.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(names)} Cardiomiopathies."))

	def create_riskfactors(self):
		"""
		Seed the Riskfactors lookup table.
		"""
		names = ["Hypertension", "Diabetes", "Smoking", "Obesity", "Hyperlipidemia"]
		for name in names:
			Riskfactors.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(names)} Riskfactors."))

	def create_comorbidities(self):
		"""
		Seed the Comorbidities lookup table.
		"""
		names = ["COPD", "CKD", "CAD", "Stroke", "Cancer"]
		for name in names:
			Comorbidities.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(names)} Comorbidities."))

	def handle(self, *args, **kwargs):
		self.stdout.write("\nPopulating database...\n")
		# Core entities
		self.create_device_types()
		self.create_therapies(30)
		self.create_doctors(10)
		self.create_genes(50)
		self.create_mutations(50)
		# self.create_studies(15)

		# Patients and related
		patients = self.create_patients(100)
		self.create_samples(patients, 300)
		self.create_research_analyses(60)

		# Procedures
		self.create_ablation_procedures(patients, 40)
		self.create_device_records(patients, 30)
		self.create_valve_interventions(patients, 30)
		self.create_coronary_interventions(patients, 30)

		# Diagnostic exams
		self.create_ecg_exams(patients, 40)
		self.create_echo_exams(patients, 40)
		self.create_rmn_tc_ph_exams(patients, 20)
		self.create_late_potentials(patients, 20)

		# Clinical
		self.create_clinical_events(patients, 20)
		self.create_clinical_evaluations(patients, 40)

		# Genetics
		self.create_genetic_profiles(patients, 30)
		self.create_genetic_samples(patients, 30)
		self.create_genetic_tests(patients, 30)
		# self.create_patient_studies(patients, 150)

		# device instances must exist
		self.create_device_events(200)

		# require patients
		self.create_symptoms()
		self.create_cardiomiopathies()
		self.create_riskfactors()
		self.create_comorbidities()

		# require patients
		self.create_ep_studies(patients, 50)
		self.create_flecainide_tests(patients, 40)
		self.create_adrenaline_tests(patients, 40)
		self.create_ajmaline_tests(patients, 40)

		# no prereqs
		self.create_genetic_statuses(patients, 90)
	
		self.stdout.write(self.style.SUCCESS("\nFake data generation completed.\n"))
		self.stdout.write(self.style.SUCCESS("✔️ Final row counts:"))
		for model in apps.get_app_config('kokoro').get_models():
			name = model.__name__
			count = model.objects.count()
			self.stdout.write(f"   {name:25} {count}")

	def create_therapies(self, count):
		for _ in range(count):
			Therapy.objects.get_or_create(name=fake.unique.word().title())

	def create_doctors(self, count):
		for _ in range(count):
			Doctors.objects.get_or_create(name=fake.name())

	def create_genes(self, count):
		for _ in range(count):
			Gene.objects.get_or_create(name=fake.unique.lexify(text='GENE_????'))

	def create_mutations(self, count):
		for _ in range(count):
			Mutation.objects.get_or_create(name=fake.unique.lexify(text='MUT_????'))

	def create_studies(self, count):
		for _ in range(count):
			start = fake.date_between(start_date='-5y', end_date='-2y')
			end = start + timedelta(days=random.randint(30, 730))
			Study.objects.get_or_create(
				project_code=fake.unique.bothify(text='CODE-####'),
				project_id=fake.unique.bothify(text='PRJ-###'),
				start_date=start,
				end_date=end
			)

	def create_patients(self, count):
		therapies = list(Therapy.objects.all())
		studies   = list(Study.objects.all())
		patients  = []

		for _ in range(count):
			dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
			patient = PatientProfile.objects.create(
				first_name     = fake.first_name(),
				last_name      = fake.last_name(),
				sex            = random.choice(['M', 'F']),
				date_of_birth  = dob,
				nation         = fake.country(),
				region         = fake.state(),
				province       = fake.city(),
				height         = random.randint(150, 200),
				weight         = random.randint(50, 120),
				cardioref_id   = fake.bothify(text='CRF-###??')
			)

			# 1–3 therapies, capped by how many we actually have:
			if therapies:
				k = random.randint(1, min(3, len(therapies)))
				patient.therapies.set(random.sample(therapies, k))

			# 0–2 allergies, capped by how many we actually have:
			if therapies:
				k = random.randint(0, min(2, len(therapies)))
				patient.allergies.set(random.sample(therapies, k))

			# 1–2 studies, capped by how many we actually have:
			if studies:
				k = 1
				patient.studies.set(random.sample(studies, k))

			patients.append(patient)

		return patients

	def create_samples(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			collection_date = fake.date_between(
				start_date=patient.date_of_birth + timedelta(days=6570), end_date='today')
			Sample.objects.create(
				patient=patient,
				imtc_id=fake.bothify(text='IMTC-####'),
				procedure_type=random.choice(['A', 'PA', 'DG']),
				informed_consent=fake.bothify(text='IC-####'),
				collection_date=collection_date,
				pbmc_vials_n=random.randint(0, 5),
				pellet_vials_n=random.randint(0, 5),
				rna_vials_n=random.randint(0, 5),
				plasma_cold_vials_n=random.randint(0, 5),
				plasma_ambient_vials_n=random.randint(0, 5),
				rin=random.randint(5, 10),
				notes=fake.sentence()
			)

	def create_research_analyses(self, count):
		samples = list(Sample.objects.all())
		for _ in range(count):
			ra = ResearchAnalysis.objects.create(
				analysis_name=fake.bs().title(),
				type=random.choice(['WGS', 'WES', 'RNAseq', 'PRO']),
				date_performed=fake.date_this_year(),
				result_files={"url": fake.url(), "id": fake.uuid4()}
			)
			ra.samples.set(random.sample(samples, k=random.randint(1, 4)))

	def create_ablation_procedures(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Ensure we only pick dates after the patient is at least 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			procedure_date = fake.date_between(start_date=start_date, end_date='today')
			Ablation.objects.create(
				patient=patient,
				date=procedure_date,
				total_area=random.uniform(5.0, 15.0),
				bas_area_a_160=random.uniform(1.0, 5.0),
				bas_area_a_180=random.uniform(1.0, 5.0),
				bas_area_a_200=random.uniform(1.0, 5.0),
				basal_pdm=random.uniform(0.5, 3.0),
				total_rf_time=random.uniform(30, 300),
				rf_w=random.uniform(20, 60),
				complication=random.choice(["Y", "N", ""]),
				complication_type=fake.sentence(nb_words=3),
				therapy=fake.word()
			)

	def create_valve_interventions(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Ensure procedures occur after the patient turns 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			procedure_date = fake.date_between(start_date=start_date, end_date='today')
			ValveIntervention.objects.create(
				patient=patient,
				date=procedure_date,
				replacement=random.choice(["Y", "N", ""]),
				repair=random.choice(["Y", "N", ""])
			)

	def create_coronary_interventions(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Ensure we only pick dates after the patient turns 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			procedure_date = fake.date_between(start_date=start_date, end_date='today')
			CoronaryIntervention.objects.create(
				patient=patient,
				date=procedure_date,
				cabg=random.choice(["Y", "N", ""]),
				pci=random.choice(["Y", "N", ""])
			)

	def create_ecg_exams(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# start only once patient is 18+
			start_date = patient.date_of_birth + relativedelta(years=18)
			exam_date = fake.date_between(start_date=start_date, end_date='today')
			ECG.objects.create(
				patient=patient,
				date_of_exam=exam_date,
				atrial_rhythmh=random.choice(['Sinus Rhythm', 'AF', 'Flutter']),
				hr=random.uniform(50, 100),
				rr=random.uniform(500, 1200),
				pq=random.uniform(100, 300),
				pr=random.uniform(100, 300),
				qrs=random.uniform(80, 120),
				qt=random.uniform(300, 500),
				qtc=random.uniform(350, 450),
				max_st=random.uniform(0, 2),
				rbbb=random.choice(["Y", "N"]),
				lrbbb=random.choice(["Y", "N"]),
				irbbb=random.choice(["Y", "N"]),
				early_rep=random.choice(["Y", "N"]),
				fragmented_qrs=random.choice(["Y", "N"]),
				brs=random.choice(["I", "II", "III"]),
				av_block=random.choice(["I", "II", "III"])
			)

	def create_echo_exams(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			start_date = patient.date_of_birth + relativedelta(years=18)
			exam_date = fake.date_between(start_date=start_date, end_date='today')
			ECHO.objects.create(
				patient=patient,date_of_exam=exam_date,
				lvef=random.uniform(40,70), tapse=random.uniform(10,30),
				left_atrial_area=random.uniform(10,30), la_diameter=random.uniform(30,50),
				la_end_diastolic_volume=random.uniform(30,60), la_end_systolic_volume=random.uniform(20,50),
				lv_end_diastolic_volume=random.uniform(100,150), lv_end_systolic_volume=random.uniform(40,80),
				lv_end_diastolic_diameter=random.uniform(40,60), lv_end_systolic_diameter=random.uniform(30,50),
				anatomical_alterations=random.choice(["Y","N"]),
				aortic_valvulopathy=random.choice(["Y","N"]),
				type_of_aortic_valvulopathy=random.choice(["Regurgitation","Stenosis","Both"]),
				severity_of_aortic_valvulopathy=random.choice(["Mild","Moderate","Severe"]),
				mitral_valvulopathy=random.choice(["Y","N"]),
				type_of_mitral_valvulopathy=random.choice(["Regurgitation","Stenosis","Both"]),
				severity_of_mitral_valvulopathy=random.choice(["Mild","Moderate","Severe"]),
				tricuspid_valvulopathy=random.choice(["Y","N"]),
				type_of_tricuspid_valvulopathy=random.choice(["Regurgitation","Stenosis","Both"]),
				severity_of_tricuspid_valvulopathy=random.choice(["Mild","Moderate","Severe"]),
				diastolic_function=random.choice(["Y","N"])
			)

	def create_rmn_tc_ph_exams(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			start_date = patient.date_of_birth + relativedelta(years=18)
			exam_date = fake.date_between(start_date=start_date, end_date='today')
			RMN_TC_PH.objects.create(
				patient=patient,date_of_exam=exam_date,
				max_pressure=random.uniform(80,160), min_pressure=random.uniform(40,100),
				anatomical_alterations=random.choice(["Y","N"]), lge=random.choice(["Y","N"]),
				type_of_lge=random.choice(["Meso","Sub-Epi","Sub-Endo"]),
				location_of_lge=random.choice(["Right","Left","Both"]) )

	def create_late_potentials(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			start_date = patient.date_of_birth + relativedelta(years=18)
			exam_date = fake.date_between(start_date=start_date, end_date='today')
			Late_potentials.objects.create(
				patient=patient,date_of_exam=exam_date,
				basal_lp1=random.uniform(0.1,5), basal_lp2=random.uniform(0.1,5),
				basal_lp3=random.uniform(0.1,5), basal_lp4=random.uniform(0.1,5)
			)

	def create_clinical_events(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Only pick dates once patient is at least 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			event_date = fake.date_between(start_date=start_date, end_date='today')
			ClinicalEvent.objects.create(
				patient=patient,
				date=event_date,
				clinical_event=random.choice(["CAR", "AR", "CT", "DEATH", "OTHER", "STROKE"]),
				cause=fake.sentence(nb_words=3),
				type=fake.word()
			)

	def create_clinical_evaluations(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			start_date = patient.date_of_birth + relativedelta(years=18)
			event_date = fake.date_between(start_date=start_date, end_date='today')
			ev = Clinical_evaluation.objects.create(
				patient=patient,date_of_visit=event_date,
				Primary_Cause_of_CD=random.choice(["Ischemic","Non Ischemic"]),
				specify_ischemic=random.choice(["CAD with Myocardial Infarction","CAD without Myocardial Infarction"]),
				mi_zone=random.choice(["Anterior","Anterolateral","Apical","Right wall","Inferior","Infero-postero lateral"]),
				specify_non_ischemic=random.choice(["dilates","hypokinetic","hypertrophic","hypertensive"]),
				nyha=random.choice(["I","II","III","IV"])
			)

	def create_genetic_profiles(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			Genetic_profile.objects.create(
				patient=patient, FIN_progressive_genetics=random.randint(1,1000),
				FIN_number=fake.bothify(text='FIN####'), PIN_number=fake.bothify(text='PIN####')
			)

	def create_genetic_samples(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Only after the patient turns 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			sample_date = fake.date_between(start_date=start_date, end_date='today')
			Genetic_sample.objects.create(
				patient=patient,
				blood_sample_date=sample_date
			)

	def create_genetic_tests(self, patients, count):
		doctors = list(Doctors.objects.all())
		genes = list(Gene.objects.all())
		mutations = list(Mutation.objects.all())
		for _ in range(count):
			patient = random.choice(patients)
			# start only once patient is 18+
			start_date = patient.date_of_birth + relativedelta(years=18)
			consent_date = fake.date_between(start_date=start_date, end_date='today')
			test = Genetic_test.objects.create(
				patient=patient,
				Consent_date=consent_date,
				processingType=random.choice(["OSR", "IMTC"]),
				testType=random.choice(["NGS", "Mutuna"]),
				test_category=random.choice([
					"Oncology",
					"Channellopathies / Arrhythmias",
					"Cardiomiopathies"
				]),
				NGStest_result=random.choice(["Positive", "Negative", "Not concluded"]),
				gene_type=random.choice(["Clinical", "Incidental"]),
				zygosity=random.choice(["HZ", "OZ", "HA"]),
				ACMG=random.choice(["I", "II", "III", "IV", "V"]),
				Mutunatest_result=random.choice(["Positive", "Negative", "Not concluded"]),
				sampleType=random.choice(["blood", "DNA"]),
				aliquota=random.randint(1, 10),
				corsa_NGS=random.choice(["Yes", "No"]),
				corsa_name=fake.bothify(text='Corsa_##'),
				sangen=random.choice(["Yes", "No"]),
				Sangen_result=random.choice(["Positive", "Negative", "Not concluded"]),
				reported=random.choice(["Yes", "No"]),
				report_data=fake.date_this_year()
			)
			test.editing_doctor.set(random.sample(doctors, k=random.randint(1, 2)))
			test.reporting_doctor.set(random.sample(doctors, k=random.randint(1, 2)))
			test.genes.set(random.sample(genes, k=random.randint(1, 3)))
			test.var_p.set(random.sample(mutations, k=random.randint(1, 2)))
			test.var_c.set(random.sample(mutations, k=random.randint(1, 2)))

	# ——— PatientStudy ———
	def create_patient_studies(self, patients, count):
		studies = list(Study.objects.all())
		if not studies:
			raise CommandError("No Study records—run create_studies first.")
		for _ in range(count):
			PatientStudy.objects.create(
				patient         = random.choice(patients),
				study           = random.choice(studies),
				enrollment_date = fake.date_between(start_date='-5y', end_date='today'),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} PatientStudy entries."))


	# ——— DeviceEvent ———
	def create_device_events(self, count):
		instances = list(DeviceInstance.objects.all())
		if not instances:
			raise CommandError("No DeviceInstance records found.")
		causes = [c[0] for c in DeviceEvent.Cause.choices]
		for _ in range(count):
			DeviceEvent.objects.create(
				device             = random.choice(instances),
				date               = fake.date_between(start_date='-1y', end_date='today'),
				n_icd_shock_appropriate_pre_rf        = random.randint(0,5),
				n_icd_shock_inappropriate_pre_rf      = random.randint(0,3),
				inappropriate_pre_rf_shock_cause      = random.choice(causes),
				n_icd_shock_appropriate_post_brs_diagnosis = random.randint(0,5),
				inappropriate_post_brs_shock_cause    = random.choice(causes),
				complications      = fake.sentence(nb_words=4),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} DeviceEvent entries."))


	# ——— Symptoms (lookup table) ———
	def seed_symptoms(self):
		names = ["Chest pain", "Dyspnea", "Palpitations", "Fatigue", "Syncope"]
		for name in names:
			Symptoms.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"Seeded {len(names)} Symptoms."))


	# ——— Cardiomiopathies (lookup table) ———
	def seed_cardiomyopathy_types(self):
		names = [
			"Dilated", "Hypertrophic", "Restrictive",
			"Arrhythmogenic RV", "Ischemic"
		]
		for name in names:
			Cardiomiopathies.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"Seeded {len(names)} Cardiomiopathies."))


	# ——— Riskfactors (lookup table) ———
	def seed_riskfactors(self):
		names = ["Hypertension", "Diabetes", "Smoking", "Obesity", "Hyperlipidemia"]
		for name in names:
			Riskfactors.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"Seeded {len(names)} Riskfactors."))


	# ——— Comorbidities (lookup table) ———
	def seed_comorbidities(self):
		names = ["COPD", "CKD", "CAD", "Stroke", "Cancer"]
		for name in names:
			Comorbidities.objects.get_or_create(name=name)
		self.stdout.write(self.style.SUCCESS(f"Seeded {len(names)} Comorbidities."))


	# ——— EP study ———
	def create_ep_studies(self, patients, count):
		results = [c[0] for c in EP_study.Result.choices]
		arrh   = [c[0] for c in EP_study.InducedAr.choices]
		for _ in range(count):
			EP_study.objects.create(
				patient            = random.choice(patients),
				date_of_provocative_test = fake.date_between(start_date='-5y', end_date='today'),
				ep_result          = random.choice(results),
				induced_arrhythmia = random.choice(arrh),
				total_area         = random.uniform(5.0, 50.0),
				bas_area_a_160     = random.uniform(5.0, 30.0),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} EP_study entries."))


	# ——— Flecainide test ———
	def create_flecainide_tests(self, patients, count):
		results = [c[0] for c in Flecainide_test.FlecResult.choices]
		for _ in range(count):
			Flecainide_test.objects.create(
				patient             = random.choice(patients),
				date_of_provocative_test = fake.date_between(start_date='-5y', end_date='today'),
				flecainide_dose     = random.uniform(0.5, 3.0),
				flecainide_result   = random.choice(results),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} Flecainide_test entries."))


	# ——— Adrenaline test ———
	def create_adrenaline_tests(self, patients, count):
		results = [c[0] for c in Adrenaline_test.AdrResult.choices]
		for _ in range(count):
			Adrenaline_test.objects.create(
				patient            = random.choice(patients),
				date_of_provocative_test = fake.date_between(start_date='-5y', end_date='today'),
				adrenaline_dose    = random.uniform(0.1, 1.0),
				adrenaline_result  = random.choice(results),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} Adrenaline_test entries."))


	# ——— Ajmaline test ———
	def create_ajmaline_tests(self, patients, count):
		results = [c[0] for c in Ajmaline_test.AjResult.choices]
		arrh    = [c[0] for c in Ajmaline_test.InducedAr.choices]
		for _ in range(count):
			Ajmaline_test.objects.create(
				patient                 = random.choice(patients),
				date_of_provocative_test= fake.date_between(start_date='-5y', end_date='today'),
				ajmaline_dose           = random.uniform(0.5, 2.0),
				ajmaline_dose_per_kg    = random.uniform(0.01, 0.05),
				ajmaline_result         = random.choice(results),
				induced_arrhythmia      = random.choice(arrh),
				bas_area_a_160          = random.uniform(5.0, 30.0),
				bas_area_a_180          = random.uniform(5.0, 30.0),
				bas_area_a_200          = random.uniform(5.0, 30.0),
				bas_area_a_250          = random.uniform(5.0, 30.0),
				bas_area_a_280_300      = random.uniform(5.0, 30.0),
				pdm                     = random.uniform(0.5, 5.0),
				brs_pattern             = random.choice([c[0] for c in Ajmaline_test.BrSpattern.choices]),
				dose_to_positive_ecg    = random.uniform(0.1, 1.0),
				time_to_positive_ecg = timedelta(seconds=random.randint(300, 3600)),
			)
		self.stdout.write(self.style.SUCCESS(f"Created {count} Ajmaline_test entries."))


	# ——— Genetic_status ———
	def create_genetic_statuses(self, patients, count):
		"""
		Create `count` Genetic_status rows, using the real field choices
		pulled from the model’s _meta rather than assuming nested-class names.
		"""
		# Grab each field’s (value,label) list from the model _meta
		meta = Genetic_status._meta
		status_choices   = [c[0] for c in meta.get_field('patient_status').choices]
		proband_choices  = [c[0] for c in meta.get_field('proband_familiarity').choices]
		famtype_choices  = [c[0] for c in meta.get_field('familiarityType').choices]
		degree_choices   = [c[0] for c in meta.get_field('family_degree').choices]

		# For the free-text phenotype fields, sample from your lookup tables:
		cardio_types = list(Cardiomiopathies.objects.values_list('name', flat=True))
		pato_types   = list(Comorbidities.objects.values_list('name', flat=True))

		for _ in range(count):
			Genetic_status.objects.create(
				patient             = random.choice(patients),
				patient_status      = random.choice(status_choices),
				proband_familiarity = random.choice(proband_choices),
				familiarityType     = random.choice(famtype_choices),
				cardio_fenotypes    = ", ".join(
										 random.sample(cardio_types,
													   k=min(2, len(cardio_types)))
									  ),
				pato_fenotypes      = ", ".join(
										 random.sample(pato_types,
													   k=min(2, len(pato_types)))
									  ),
				family_members      = random.randint(0, 10),
				family_degree       = random.choice(degree_choices),
				children            = random.randint(0, 5),
			)
		self.stdout.write(
			self.style.SUCCESS(f"Created {count} Genetic_status entries.")
		)

