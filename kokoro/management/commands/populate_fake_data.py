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
	Genetic_sample, Genetic_test
)

fake = Faker()

class Command(BaseCommand):
	help = "Populate database with realistic fake data for testing"

	def handle(self, *args, **kwargs):
		self.stdout.write("\nPopulating database...\n")
		# Core entities
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
		self.create_device_implants(patients, 30)
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

		self.stdout.write(self.style.SUCCESS("\nFake data generation completed.\n"))

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
		studies = list(Study.objects.all())
		patients = []
		for _ in range(count):
			dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
			patient = PatientProfile.objects.create(
				first_name=fake.first_name(),
				last_name=fake.last_name(),
				sex=random.choice(['M', 'F']),
				date_of_birth=dob,
				nation=fake.country(),
				region=fake.state(),
				province=fake.city(),
				height=random.randint(150, 200),
				weight=random.randint(50, 120),
				cardioref_id=fake.bothify(text='CRF-###??')
			)
			patient.therapies.set(random.sample(therapies, random.randint(1, 3)))
			patient.allergies.set(random.sample(therapies, random.randint(0, 2)))
			patient.studies.set(random.sample(studies, random.randint(1, 2)))
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

	def create_device_implants(self, patients, count):
		for _ in range(count):
			patient = random.choice(patients)
			# Ensure we only pick dates after the patient turns 18
			start_date = patient.date_of_birth + relativedelta(years=18)
			implant_date = fake.date_between(start_date=start_date, end_date='today')
			DeviceImplant.objects.create(
				patient=patient,
				date=implant_date,
				lv4_ring=random.uniform(20, 50),
				lv3_ring=random.uniform(20, 50),
				lv2_ring=random.uniform(20, 50),
				lv1_tip=random.uniform(20, 50),
				v1=random.uniform(0.1, 5.0),
				ms1=random.randint(0, 10),
				lv_pulse_configuration_2_lv2=random.uniform(20, 50),
				pacing_impendance1=random.uniform(300, 1000),
				v2=random.uniform(0.1, 5.0),
				ms2=random.randint(0, 10),
				pacing_impendance2=random.uniform(300, 1000),
				v3=random.uniform(0.1, 5.0),
				ms3=random.randint(0, 10),
				pacing_impendance3=random.uniform(300, 1000)
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
