from django.db import models
import uuid
import datetime
from dateutil.relativedelta import relativedelta




#######################################################################
############################## THERAPIES ##############################
#######################################################################

class Therapy(models.Model):
	"""
	A single therapy or medication.
	"""
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Therapy'
		verbose_name_plural = 'Therapies'

	def __str__(self):
		return self.name




###############################################################################
############################### PATIENT PROFILE ###############################
###############################################################################

# "Patient" eredita da "models.Model", quindi sarà mappato in una tabella del database.
class Study(models.Model):

	id = models.UUIDField(
	# "primary_key=True": indica che questo è il campo identificativo unico della tabella.
	primary_key = True,
	# "default=uuid.uuid4": genera un nuovo UUID ogni volta che viene creato un oggetto.
	default = uuid.uuid4,
	# "editable=False": impedisce la modifica del campo tramite interfaccia admin o form.
	editable = False
	)
	project_code = models.CharField(max_length=100, unique=True)
	project_id = models.CharField(max_length=100)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	
	class Meta:
		verbose_name = 'Study'
		verbose_name_plural = 'Studies'

	def __str__(self):
		return self.project_id


class PatientProfile(models.Model):
	# UUIDField: campo che contiene un UUID (Universal Unique Identifier).
	id = models.UUIDField(
		# "primary_key=True": indica che questo è il campo identificativo unico della tabella.
		primary_key = True,
		# "default=uuid.uuid4": genera un nuovo UUID ogni volta che viene creato un oggetto.
		default = uuid.uuid4,
		# "editable=False": impedisce la modifica del campo tramite interfaccia admin o form.
		editable = False
		)
	
	# TextChoices: modo elegante per definire scelte enumerate leggibili dall'utente.
	class Sex(models.TextChoices):
		# M e F sono valori memorizzati nel DB.
		# "Male" e "Female" sono le etichette leggibili.
		MAN = "M", "Male"
		WOMAN = "F", "Female"
			
	# CharField: campo stringa, con lunghezza massima di 100 caratteri.        
	last_name = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	
	# choices=Sex: obbliga l’utente a selezionare uno dei valori definiti nella classe Sex.
	sex = models.CharField(
		max_length=1,
		choices=Sex
		)
	date_of_birth = models.DateField()
	nation = models.CharField(max_length=100, blank=True, default='')
	region = models.CharField(max_length=100, blank=True, default='')
	province = models.CharField(max_length=100, blank=True, default='')
	height = models.PositiveIntegerField(null=True, blank=True)
	weight = models.PositiveIntegerField(null=True, blank=True)
	cardioref_id = models.PositiveIntegerField(null=True, blank=True)

	therapies = models.ManyToManyField(
		Therapy,
		blank=True,
		related_name='patients_therapies',
		help_text='Therapies this patient is on.'
	)

	allergies = models.ManyToManyField(
		Therapy,
		blank=True,
		related_name='patient_allergies',
		help_text='Patient\'s allergies'
	)

	studies = models.ManyToManyField(
		Study,
		related_name='participants',
		blank=True,
		help_text='Which studies this patient is enrolled in'
	)

	class Meta:
		verbose_name = "Patient Profile"
		verbose_name_plural = "Patient Profiles"  # Fixes incorrect pluralization
		# permissions: aggiunge un permesso personalizzato che potrà essere usato per controllare l’accesso a dati sensibili.
		permissions = [
		("access_sensible_info", "Can view patient sensible info")
		]

	def get_absolute_url(self):
		return reverse("kokoro:patient_detail", kwargs={"pk": self.pk})

	def __str__(self):
		parts = [self.last_name, self.first_name]
		if self.cardioref_id:
			parts.append(f"(ID: {self.cardioref_id})")
		return " ".join(filter(None, parts))


# Needed to be able to track enrollment date
class PatientStudy(models.Model):
	patient         = models.ForeignKey(
						  PatientProfile,
						  on_delete=models.CASCADE,
						  related_name='patient_studies'
					  )
	study           = models.ForeignKey(
						  Study,
						  on_delete=models.CASCADE,
						  related_name='study_participants'
					  )
	enrollment_date = models.DateField()

	class Meta:
		unique_together = ('patient', 'study') # The same patient can't be enrolled twice in the same study
		ordering        = ['-enrollment_date']

	def __str__(self):
		return f"{self.patient} ↔ {self.study} on {self.enrollment_date}"




###############################################################################
################################# PROCEDURES ##################################
###############################################################################

# Procedures common fields are defined in a base class which is then inherited by single procedures
class ProcedureBase(models.Model):

	## IMPORTANT!!!
	## Ablation is accessible as Profile_patient.ablation_set.all()
	## DeviceImplant as Profile_patient.DeviceImplant_set.all()

	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
	)

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)
	date = models.DateField() # This substitute ablation date, implant date and so on...

	class Meta:
		abstract = True # Tell django this is an abstract class, no table will be created


class Ablation(ProcedureBase):

	class Complication(models.TextChoices):
		YES = "Y", "Yes"
		NO = "N", "No"

	# Ablation done is not needed
	# Date is inherited
	total_area = models.FloatField(null=True, blank=True)
	bas_area_a_160 = models.FloatField(null=True, blank=True) # what bas means? 'a' means above (>160)
	bas_area_a_180 = models.FloatField(null=True, blank=True) # what bas means? 'a' means above (>180)
	bas_area_a_200 = models.FloatField(null=True, blank=True) # what bas means? 'a' means above (>200)
	basal_pdm = models.FloatField(null=True, blank=True)
	total_rf_time = models.FloatField(null=True, blank=True)
	rf_w = models.FloatField(null=True, blank=True)

	complication = models.CharField(
		max_length=2,
		choices=Complication.choices,
		blank=True,
		default="",
	)

	complication_type = models.CharField(
		max_length=250,
		blank=True,
		default="",
	)

	therapy = models.CharField(
		max_length=250,
		blank=True,
		default="",
	)

	class Meta:
		verbose_name = 'Ablation'
		verbose_name_plural = 'Ablations'

	def __str__(self):
		return f"{self.patient} on {self.date}"

class DeviceType(models.Model):

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)
	class Design(models.TextChoices):
		EMPTY = '', 'Choose a design'
		SD_PACEMAKER = "Single\\Dual Pacemaker"
		SD_CHAMBER_ICD = "Single\\Dual Chamber ICD"
		OTHER = "Other"

	class Model(models.TextChoices):
		EMPTY = '', 'Choose a model'
		IN7F4IS4 = "INTICA 7 HF-TQPDF4/IS4"
		RI7HFQP = "RIVACOR 7 HF-T QP"
		IN7HFIS4 = "INTICA 7 HF-TQPDF1/IS4"
		INN7HFQP = "INTICA NEO 7 HF-T QP"

	class Type(models.TextChoices):
		EMPTY = '', 'Choose a type'
		CARDIAC_DEVICE = "CD", "Cardiac Device"
		LOOP_RECORDER = "LR", "Loop Recorder"
		PACE_MAKER = "PM", "Pace Maker"

	class Company(models.TextChoices):
		EMPTY = '', 'Choose a company'
		ABBOTT = "AB", "Abbott"
		BIOTRONIK = "BT", "Biotronik"
		MEDTRONIC = "MT", "Medtronic"
		BOSTON = "BS", "Boston"
		STJUDE = "SJ", "St. Jude"

	type = models.CharField(
		max_length=5,
		choices=Type.choices,
		blank=False,
	)
	company = models.CharField(
		max_length=50,
		choices=Company.choices,
		blank=False,
	)

	model = models.CharField(
		max_length=50,
		choices=Model.choices,
		blank=False,
	)
	design = models.CharField(
		max_length=50,
		choices=Design.choices,
		blank=False,
		)# I'm calling it design because i can't find a more appropriate name rn

	class Meta:
		verbose_name = 'Device Type'
		verbose_name_plural= 'Device Types'

	def __str__(self):
		return f"{self.type}, {self.model}, ({self.company})"

class DeviceInstance(models.Model):
	
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	device_type = models.ForeignKey(
		DeviceType,
		on_delete=models.PROTECT,
		related_name="device",
	)	

	serial_number = models.CharField( ## Most probably i didn't got which field contains the serial, i need to ask.
		max_length=100, 
		unique=True,
		help_text="Unique identifier printed on the device"
	)

	patient = models.ForeignKey(
		PatientProfile,
		on_delete=models.CASCADE,
		related_name="patient",
	)

	class Meta:
		verbose_name = 'Device instance'
		verbose_name_plural= 'Device instances'

	def __str__(self):
		return f"{self.device_type.model} SN:{self.serial_number}"

class DeviceImplant(ProcedureBase):

	# SET KEYS
	device_instance = models.OneToOneField(
		DeviceInstance,
		on_delete=models.CASCADE,
		related_name='implant'
		)
	# CONDUCTION TIMES RV-PACED TO LV-SENSED
	lv4_ring = models.FloatField(null=True, blank=True)
	lv3_ring = models.FloatField(null=True, blank=True)
	lv2_ring = models.FloatField(null=True, blank=True)
	lv1_tip = models.FloatField(null=True, blank=True)
	# CONDUCTION TIMES RV-SENSED TO LV-SENSED
	# PACING CAPTURE THRESHOLD--1
	v1 =  models.FloatField(null=True, blank=True)
	ms1 = models.PositiveIntegerField(null=True, blank=True)
	lv_pulse_configuration_2_lv2 = models.FloatField(null=True, blank=True)
	pacing_impendance1 = models.FloatField(null=True, blank=True)
	# PACING CAPTURE THRESHOLD--2
	v2 =  models.FloatField(null=True, blank=True)
	ms2 = models.PositiveIntegerField(null=True, blank=True)
	# RV CHANNEL
	pacing_impendance2 = models.FloatField(null=True, blank=True)
	# PACING CAPTURE THRESHOLD--3
	v3 =  models.FloatField(null=True, blank=True)
	ms3 = models.PositiveIntegerField(null=True, blank=True)	
	# Are these fieds (ms, V) repeated or are they needed, or this needs to be logged?
	# A CHANNEL
	pacing_impendance3 = models.FloatField(null=True, blank=True)

	class Meta:
		verbose_name = 'Device implant'
		verbose_name_plural= 'Device implants'

	def __str__(self):
		return f"Implant on {self.date} for {self.patient}"


class ValveIntervention(ProcedureBase):

	class ReplacementRepair(models.TextChoices):
		YES = "Y", "Yes"
		NO = "N", "No"

	replacement = models.CharField(
		max_length=1,
		choices=ReplacementRepair.choices,
		blank=True,
		default="",
	)

	repair = models.CharField(
		max_length=1,
		choices=ReplacementRepair.choices,
		blank=True,
		default="",
	)


class CoronaryIntervention(ProcedureBase):

	class CabgPci(models.TextChoices):
		YES = "Y", "Yes"
		NO = "N", "No"

	# Coronary Artery Bypass Graft
	cabg = models.CharField( 
		max_length=1,
		choices=CabgPci.choices,
		blank=True,
		default="",
	)

	# Percutaneous coronary intervention
	pci = models.CharField(
		max_length=1,
		choices=CabgPci.choices,
		blank=True,
		default="",
	)




###############################################################################
################################### DEVICES ###################################
###############################################################################


class DeviceEvent(models.Model):

	class Cause(models.TextChoices):
		TPSV = "TSPV", "TPSV"
		FA = "FA", "FA"
		RV_LEAD_MAL = "LEMA", "Malfunzionamento elettrocatetere vd"
		ATRIAL_FLUTTER = "FLU", "Flutter Atriale"
		LEAD_MACRODISP = "MAC", "Macrodislocazione Elettrocatetere"
		SINUS_TACHY = "SIN", "Tachicardia Sinusale"
		NOISE = "N", "Rumore"
		AIR_BUBBLE = "AB", "Bolla d'aria"
		RV_LEAD_DISLO = "DIS", "Dislocazione elettrodo VD"
		T_DOUBLE = "TD", "T double counting"
		TV_A_FV = "TVTF", "TV>FV"
		UNKNOWN = "UNK", "Sconosciuto"

	# Link back to your unique device instance
	device = models.ForeignKey(
		"DeviceInstance",
		on_delete=models.CASCADE,
		related_name="event",
	)

	# Internal Date, potentially can be used to check if date was inserted correctly
	timestamp = models.DateTimeField(auto_now_add=True)
	date = models.DateField()

	n_icd_shock_appropriate_pre_rf = models.PositiveIntegerField(null=True, blank=True)
	n_icd_shock_inappropriate_pre_rf = models.PositiveIntegerField(null=True, blank=True)
	inappropriate_pre_rf_shock_cause = models.CharField(
		max_length=4,
		choices=Cause.choices,
		blank=True,
		default="",
	)
	n_icd_shock_appropriate_post_brs_diagnosis = models.PositiveIntegerField(null=True, blank=True)
	inappropriate_post_brs_shock_cause = models.CharField(
		max_length=4,
		choices=Cause.choices,
		blank=True,
		default="",
	)
	complications = models.CharField(max_length=250, blank=True, default='')
	
	class Meta:
		ordering = ["-timestamp"]

	def __str__(self):
		return f"{self.device} @ {self.timestamp:%Y-%m-%d %H:%M}"




###############################################################################
################################### SAMPLES ###################################
###############################################################################

class Sample(models.Model):
	# Type may be missing (perfieral blood, pericardial fluid)

	# Choices for procedure_type field
	class ProcedureType(models.TextChoices):
		ABLATION = "A", "Ablation"
		ABLATION_FOLLOW_UP = "PA", "Post-ablation follow-up"
		DIAGNOSIS = "DG", "Diagnosis"

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
		related_name="samples",
	)

	imtc_id = models.CharField(
		max_length=20,  # id_sample in canva
	)

	# First registration date: what is that? I think it can be inherited from PatientProfile?
	procedure_type = models.CharField(
		max_length=2,
		choices=ProcedureType.choices,
		blank=True,
		default="",
	)

	informed_consent = models.CharField(max_length=20)
	collection_date = models.DateField() # sample_collection_date in canva
	pbmc_vials_n = models.PositiveIntegerField(null=True, blank=True)
	# total_pbmc can be calculated in view, no need for an entry
	pellet_vials_n = models.PositiveIntegerField(null=True, blank=True)
	rna_vials_n = models.PositiveIntegerField(null=True, blank=True)
	plasma_cold_vials_n = models.PositiveIntegerField(null=True, blank=True)
	plasma_ambient_vials_n = models.PositiveIntegerField(null=True, blank=True)
	# skipped ajmaline test result, this is not the right place
	rin = models.PositiveIntegerField(null=True, blank=True)
	notes = models.CharField(
		max_length=250,
		blank=True,
	)

	class Meta:
		verbose_name = 'Sample'
		verbose_name_plural = 'Samples'

	def __str__(self):
		return f"{self.imtc_id} ({self.get_procedure_type_display()})"


#################### IMTC ####################
class ResearchAnalysis(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	class AnalysisType(models.TextChoices):
		whole_genome_sequencing = "WGS", "Whole Genome Sequencing"
		whole_exome_sequencing = "WES", "Whole Exome Sequencing"
		rna_sequencing = "RNAseq", "RNA sequencing"
		proteomics = "PRO", "Proteomics (Mass Spectrometry)"

	analysis_name = models.CharField(
		max_length=250,
		blank=True,
		help_text="Analysis name"
	)

	type = models.CharField(
		max_length=10,
		choices=AnalysisType,
		help_text="Type of omics analysis performed"
	)

	samples = models.ManyToManyField(
		Sample,
		related_name="analyses",
		help_text="Samples used in this analysis"
	)

	date_performed = models.DateField(auto_now_add=True)

	# Campo JSON per salvare i risultati (link, path, ID, ecc.).
	result_files = models.JSONField(
		blank=True,
		null=True,
		help_text="Paths or identifiers for result files"
	)

	class Meta:
		verbose_name = "Omics Analysis"
		verbose_name_plural = "Omics Analyses"  # Fixes incorrect pluralization

	def __str__(self):
		return f"{self.get_type_display()} ({self.date_performed})"	




######################################################################################
################################### CLINICAL STATUS ##################################
#####################################################################################

class Clinical_Status(models.Model):
	
	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
	)

	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)
	
	
	# !!! This date format is not optimal, it should be changed !!!
	date_of_visit = models.DateField()
	
	class Meta:
		abstract = True # N.B. Tell django this is an abstract class, no table will be created


class Symptoms(models.Model):

	name = models.CharField(max_length=100, unique=True, default='')

	class Meta:
		ordering = ['name']
		verbose_name = 'Symptom'
		verbose_name_plural= 'Symptoms'

	def __str__(self):
		return self.name
	

class Cardiomiopathies(models.Model):

	name = models.CharField(max_length=100, unique=True, default='')

	class Meta:
		ordering = ['name']
		verbose_name = 'Cardiomiopathy'
		verbose_name_plural= 'Cardiomiopathies'

	def __str__(self):
		return self.name
	

class Riskfactors(models.Model):

	name = models.CharField(max_length=100, unique=True, default='')

	class Meta:
		ordering = ['name']
		verbose_name = 'Risk factor'
		verbose_name_plural= 'Risk factors'

	def __str__(self):
		return self.name


class Comorbidities(models.Model):

	name = models.CharField(max_length=100, unique=True, default='')

	class Meta:
		ordering = ['name']
		verbose_name = 'Comorbidity'
		verbose_name_plural= 'Comorbidities'
	def __str__(self):
		return self.name

class ClinicalEvent(models.Model):

	class Cause(models.TextChoices):
		CAR = "CAR", "Cardiac arrest resuscitated"
		AR = "AR", "Arrhytmia"
		CT = "CT", "Cardiac transplant"
		DEATH = "DEATH", "Death"
		OTHER = "OT", "Other"
		STROKE = "STROKE", "Stroke"

	# Link back to your unique device instance
	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
		related_name="clinical_event",
	)

	# Internal Date, potentially can be used to check if dat was inserted correctly
	timestamp = models.DateTimeField(auto_now_add=True)
	date = models.DateField()

	clinical_event = models.CharField(
		max_length=100,
		choices=Cause.choices,
		blank=True,
		default="",
	)

	cause = models.CharField(
		max_length=100,
		blank=True,
		default="",
	)

	type = models.CharField(
		max_length=100,
		blank=True,
		default="",
	)

	class Meta:
		verbose_name = 'Clinical Event'
		verbose_name_plural= 'Clinical Events'

	def __str__(self):
		return f"{self.get_clinical_event_display()} @ {self.timestamp:%Y-%m-%d %H:%M}"
		
class Clinical_evaluation(Clinical_Status):

	symptoms = models.ManyToManyField(
		Symptoms,
		blank=True,
		related_name='clinical_evaluation',
		help_text='Symptoms this patient have.'
	)

	cardiomiopathies = models.ManyToManyField(
		Cardiomiopathies,
		blank=True,
		related_name='clinical_evaluation',
		help_text='Cardiomiopathies this patient have.'
	)

	riskfactors = models.ManyToManyField(
		Riskfactors,
		blank=True,
		related_name='clinical_evaluation',
		help_text='Risk Factors of this patient.'
	)

	comorbidities = models.ManyToManyField(
		Comorbidities,
		blank=True,
		related_name='clinical_evaluation',
		help_text='Comorbidities this patient have.'
	)
 
	# Are there only 2 possible options for primary cause of cardiovascular disease?
	class PRIcauseCD(models.TextChoices):
		I = "Ischemic", "Ischemic"
		NI = "Non Ischemic", "Non Ischemic"

	Primary_Cause_of_CD = models.CharField(
		max_length=13,
		choices=PRIcauseCD,
		default=''
	)

	# !!! Only if "Ischemic" is selected, these should be compiled !!!
	class Ischemic(models.TextChoices):
		my = "CAD with Myocardial Infarction", "CAD with Myocardial Infarction"
		non_my = "CAD without Myocardial Infarction", "CAD without Myocardial Infarction"
	specify_ischemic = models.CharField(
		max_length=100,
		choices=Ischemic,
		default=''
		
	)
	# !!! Only if "my" is selected, this should be compiled !!!
	class MiZone(models.TextChoices):
		an = "Anterior", "Anterior"
		anla = "Anterolateral", "Anterolateral"
		ap = "Apical", "Apical" 
		rw = "Right wall", "Right wall"
		inf = "Inferior", "Inferior"
		infpola = "Infero-postero lateral", "Infero-postero lateral"
	mi_zone = models.CharField(
		max_length=100,
		choices=MiZone,
		default=''
	)

	# !!! Only if "Non Ischemic" is selected, this should be compiled !!!
	class NonIschemic(models.TextChoices):
		d = "dilates", "dilates"
		hk = "hypokinetic", "hypokinetic"
		hp = "hypertrophic", "hypertrophic"
		ht = "hypertensive", "hypertensive"
	specify_non_ischemic = models.CharField(
		max_length=100,
		choices=NonIschemic,
		default=''
	)

	# NYHA = New York Heart Association
	class NYHA(models.TextChoices):
		U = "I", "I"
		D = "II", "II"
		T = "III", "III"
		Q = "IV", "IV"
	nyha = models.CharField(
		max_length=4,
		choices=NYHA,
		default=''
	)	
	class Meta:
		verbose_name = 'Clinical Evaluation'
		verbose_name_plural= 'Clinical Evaluations'



#####################################################################################
################################ PROVOCATIVE TESTS ##################################
#####################################################################################
### \\\ It should contain a model for each type of test:
### \\\ - Electrophysiological study (EP study)
### \\\ - Ajmaline test
### \\\ - Flecainide test
### \\\ - Adrenaline test

class Provocative_tests(models.Model):
	
	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
	)

	# mi serve ancora?
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)
	
	# !!! Only if "Yes" is selected, these should be compiled !!!
	date_of_provocative_test = models.DateField()
	
	class Meta:
		abstract = True # Tell django this is an abstract class, no table will be created


class EP_study(Provocative_tests):

	class Result(models.TextChoices):
		Po = "Positive", "Positive"
		Ne = "Negative", "Negative"	
	ep_result = models.CharField(
		max_length=9,
		choices=Result
	)
	# !!! Only if "Yes" is selected, these should be compiled !!!
	class InducedAr(models.TextChoices):
		VF = "VF", "VF"
		NSVF = "NSVF", "NSVF"
		VFNS = "VFNS", "VFNS"
		VT = "VT", "VT"
		VTNS = "VTNS", "VTNS"
	induced_arrhythmia = models.CharField(
		max_length=9,
		choices=InducedAr,
		default=''
	)

	# !!! BASALE, AJMALINA, APEX, RVOT, DRIVE, 1° EXTRAST, 2° EXTRAST, 3° EXTRAST... what are they for ? !!!

	total_area = models.FloatField(null=True, blank=True) # measure unit cm^2
	bas_area_a_160 = models.FloatField(null=True, blank=True)


class Flecainide_test(Provocative_tests):

	flecainide_dose = models.FloatField(null=True, blank=True)
	class FlecResult(models.TextChoices):
		Po = "Positive", "Positive"
		Ne = "Negative", "Negative"	
	flecainide_result = models.CharField(
		max_length=9,
		choices=FlecResult,
		default=''
	)
	class Meta:
		verbose_name = 'Flecainide test'
		verbose_name_plural = 'Flecainide tests'

class Adrenaline_test(Provocative_tests):

	adrenaline_dose = models.FloatField(null=True, blank=True)
	class AdrResult(models.TextChoices):
		Po = "Positive", "Positive"
		Ne = "Negative", "Negative"	
		W = "Weakly positive", "Weakly positive"
	adrenaline_result = models.CharField(
		max_length=16,
		choices=AdrResult,
		default=''
	)
	class Meta:
		verbose_name = 'Adrenaline test'
		verbose_name_plural = 'Adrenaline tests'
	# !!! In Canva there are other options.. do we want to include them? (e.g. LQT 3)


class Ajmaline_test(Provocative_tests):

	ajmaline_dose = models.FloatField(null=True, blank=True)
	ajmaline_dose_per_kg = models.FloatField(null=True, blank=True)
	class AjResult(models.TextChoices):
		Po = "Positive", "Positive"
		Ne = "Negative", "Negative"	
		W = "Weakly positive", "Weakly positive"
	ajmaline_result = models.CharField(
		max_length=16,
		choices=AjResult,
		default=''
	)
	# !!! In Canva, there are also other options... should we also include them? !!!
	# J wave, Long QT, Spontaneous type I 
	class InducedAr(models.TextChoices):
		VF = "VF", "VF"
		NSVF = "NSVF", "NSVF"
		VFNS = "VFNS", "VFNS"
		VT = "VT", "VT"
		VTNS = "VTNS", "VTNS"
	induced_arrhythmia = models.CharField(
		max_length=5,
		choices=InducedAr,
		default=''
	)
	
	bas_area_a_160 = models.FloatField(null=True, blank=True) #'a' means above (>160)
	bas_area_a_180 = models.FloatField(null=True, blank=True) # 'a' means above (>180)
	bas_area_a_200 = models.FloatField(null=True, blank=True) # 'a' means above (>200)
	bas_area_a_250 = models.FloatField(null=True, blank=True) # 'a' means above (>250)
	bas_area_a_280_300 = models.FloatField(null=True, blank=True) # 'a' means above (>280 / 300)
	pdm = models.FloatField(null=True, blank=True) # !!! what does pmd stands for? !!!
	# !!! In Canva, these values are doubled in case of redo... how to create kind of a log? !!!

	class BrSpattern(models.TextChoices):
		U = "I", "I"
		D= "II", "II"
		T = "III", "III"
		S = "Suspect", "Suspect"
	brs_pattern = models.CharField(
		max_length=8,
		choices=BrSpattern,
		default=''
	)

	# !!! What do these 2 voices mean? !!!
	dose_to_positive_ecg = models.FloatField(null=True, blank=True)	
	time_to_positive_ecg = models.DurationField(null=True, blank=True)




#####################################################################################
################################### DIAGNOSTIC EXAMS ################################
#####################################################################################
### \\\ It should contain a model for each type of exam:
### \\\ - ECG
### \\\ - ECHO
### \\\ - Late potentials
### \\\ - RMN / TC / PH
class Diagnostic_exams(models.Model):
	
	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
	)

	# mi serve ancora?
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)
	
	date_of_exam = models.DateField()

	# !!! In Canva, they are collected in a separated section, but I don't think a specific model is necessary !!!
	# Shouln't these values be seen in "Clinical status" page and be related to a visit?
	max_pressure = models.FloatField(null=True, blank=True)	
	min_pressure = models.FloatField(null=True, blank=True)	

	class Meta:
		abstract = True # Tell django this is an abstract class, no table will be created


class ECG(Diagnostic_exams):

	class Atrialrhythm(models.TextChoices):
		SR = "Sinus Rhythm", "Sinus Rhythm"
		AF = "AF", "AF"
		FU = "Flutter", "Flutter"	
	atrial_rhythmh = models.CharField(
		max_length=100,
		choices=Atrialrhythm,
		default=''
	)

	ecg_file = models.FileField(upload_to='ecg_data/', null=True, blank=True)
	hr = models.FloatField(null=True, blank=True)
	rr = models.FloatField(null=True, blank=True) # measure unit in ms
	pq = models.FloatField(null=True, blank=True) # measure unit in ms
	pr = models.FloatField(null=True, blank=True) # measure unit in ms
	# !!! Do we need "INTRINSIC PR INTERVAL DURING ATRIAL SENSED" & "INTRINSIC PR INTERVAL DURING ATRIAL PACED" ? !!!


	qrs = models.FloatField(null=True, blank=True) # measure unit in ms
	qt = models.FloatField(null=True, blank=True) # measure unit in ms
	qtc = models.FloatField(null=True, blank=True) # measure unit in ms
	max_st = models.FloatField(null=True, blank=True) # measure unit in mV
	# !!! In Canva, these values are doubled because we need to know them both before and after Ajmaline test 
	# how can we create the log? !!!


	# !!! Do we want specific options for specific BBB or do we want a unique elencation? !!!
	class RBBB(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	rbbb = models.CharField(
		max_length=3,
		choices=RBBB,
		default=''
	)
	class LRBBB(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	lrbbb = models.CharField(
		max_length=3,
		choices=LRBBB,
		default=''
	)
	class IRBBB(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	irbbb = models.CharField(
		max_length=3,
		choices=IRBBB,
		default=''
	)

	class EarlyRep(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	early_rep = models.CharField(
		max_length=3,
		choices=EarlyRep,
		default=''
	)

	class FragQRS(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	fragmented_qrs = models.CharField(
		max_length=3,
		choices=FragQRS,
		default=''
	)

	# !!! What does BRS stand for? !!!
	class BRS(models.TextChoices):
		U = "I", "I"
		D= "II", "II"
		T = "III", "III"
	brs = models.CharField(
		max_length=4,
		choices=BRS,
		default=''
	)

	class AVblock(models.TextChoices):
		U = "I", "I"
		D= "II", "II"
		T = "III", "III"
	av_block = models.CharField(
		max_length=14,
		choices=AVblock,
		default=''
	)
	class Meta:
		verbose_name = 'ECG'
		verbose_name_plural= 'ECGs'

class ECHO(Diagnostic_exams):

	lvef = models.FloatField(null=True, blank=True)
	tapse = models.FloatField(null=True, blank=True)
	left_atrial_area = models.FloatField(null=True, blank=True) # measure unt in cm^2
	la_diameter = models.FloatField(null=True, blank=True)
	la_end_diastolic_volume = models.FloatField(null=True, blank=True)
	la_end_systolic_volume = models.FloatField(null=True, blank=True)
	lv_end_diastolic_volume = models.FloatField(null=True, blank=True)
	lv_end_systolic_volume = models.FloatField(null=True, blank=True)
	lv_end_diastolic_diameter = models.FloatField(null=True, blank=True)
	lv_end_systolic_diameter = models.FloatField(null=True, blank=True)

	class AnatomicalAlterations(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	anatomical_alterations = models.CharField(
		max_length=3,
		choices=AnatomicalAlterations,
		default=''
	)


	# !!! Instead of creating 3 different classes of questions for 3 different valves,
	# we could create one collective voice called "type_of_valve" and 3 answers (aortic, mitral & tricuspid) !!!
	class AorticValvulopathy(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	aortic_valvulopathy = models.CharField(
		max_length=3,
		choices=AorticValvulopathy,
		default=''
	)
	class AorticValvulopathyType(models.TextChoices):
		R = "Regurgitation", "Regurgitation"
		S = "Stenosis", "Stenosis"
		B = "Both", "Both"	
	type_of_aortic_valvulopathy = models.CharField(
		max_length=13,
		choices=AorticValvulopathyType,
		default=''
	)
	# !!! How can we handle severity in case of both? !!!
	class AorticValvulopathySeverity(models.TextChoices):
		Mi = "Mild", "Mild"
		Mo = "Moderate", "Moderate"
		Se = "Severe", "Severe"	
	severity_of_aortic_valvulopathy = models.CharField(
		max_length=13,
		choices=AorticValvulopathySeverity,
		default=''
	)

	class MitralValvulopathy(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	mitral_valvulopathy = models.CharField(
		max_length=3,
		choices=MitralValvulopathy,
		default=''
	)

	class MitralValvulopathyType(models.TextChoices):
		R = "Regurgitation", "Regurgitation"
		S = "Stenosis", "Stenosis"
		B = "Both", "Both"	
	type_of_mitral_valvulopathy = models.CharField(
		max_length=13,
		choices=MitralValvulopathyType,
		default=''
	)

	# !!! How can we handle severity in case of both? !!!
	class MitralValvulopathySeverity(models.TextChoices):
		Mi = "Mild", "Mild"
		Mo = "Moderate", "Moderate"
		Se = "Severe", "Severe"	
	severity_of_mitral_valvulopathy = models.CharField(
		max_length=13,
		choices=MitralValvulopathySeverity,
		default=''
	)

	class TricuspidValvulopathy(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	tricuspid_valvulopathy = models.CharField(
		max_length=3,
		choices=TricuspidValvulopathy,
		default=''
	)

	class TricuspidValvulopathyType(models.TextChoices):
		R = "Regurgitation", "Regurgitation"
		S = "Stenosis", "Stenosis"
		B = "Both", "Both"	
	type_of_tricuspid_valvulopathy = models.CharField(
		max_length=13,
		choices=TricuspidValvulopathyType,
		default=''
	)

	# !!! How can we handle severity in case of both? !!!
	class TricuspidValvulopathySeverity(models.TextChoices):
		Mi = "Mild", "Mild"
		Mo = "Moderate", "Moderate"
		Se = "Severe", "Severe"	
	severity_of_tricuspid_valvulopathy = models.CharField(
		max_length=13,
		choices=TricuspidValvulopathySeverity,
		default=''
	)

	class DiastolicDysfunction(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	diastolic_function = models.CharField(
		max_length=3,
		choices=DiastolicDysfunction,
		default=''
	)

	# !!! what are TIPO_34 and EF ? Do we need them ? !!!
	class Meta:
		verbose_name = 'Ecography'
		verbose_name_plural= 'Ecography'


class Late_potentials(Diagnostic_exams):

	basal_lp1 = models.FloatField(null=True, blank=True)
	basal_lp2 = models.FloatField(null=True, blank=True)
	basal_lp3 = models.FloatField(null=True, blank=True)
	basal_lp4 = models.FloatField(null=True, blank=True)
	# !!! I wrote only 4 values (the basal one), but they should be re-collected during each follow-up...
	# how to create a log ? !!!	
	class Meta:
		verbose_name = 'Late potential'
		verbose_name_plural = 'Late potentials'


class RMN_TC_PH(Diagnostic_exams):

	class AnatomicalAlterations(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	anatomical_alterations = models.CharField(
		max_length=3,
		choices=AnatomicalAlterations,
		default=''
	)

	class LGE(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	lge = models.CharField(
		max_length=3,
		choices=LGE,
		default=''
	)
	# !!! Only if "Yes" is selected, these should be compiled !!!
	class LGEType(models.TextChoices):
		Me = "Meso", "Meso"
		SubEpi = "Sub-Epi", "Sub-Epi"
		SubEndo = "Sub-Endo", "Sub-Endo"	
	type_of_lge = models.CharField(
		max_length=9,
		choices=LGEType,
		default=''
	)
	class LGElocation(models.TextChoices):
		R = "Right", "Right"
		L = "Left", "Left"
		B = "Both", "Both"	
	location_of_lge = models.CharField(
		max_length=5,
		choices=LGElocation,
		default=''
	)





#####################################################################################
################################### AUXILIAR FUNCTIONS ##############################
#####################################################################################


#################### CARDIO FENOTYPES ####################

# class Cardio_Fenotypes(models.Model):
# 	"""
# 	A single cardiopathy fenotype.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'Cardiopathy Fenotype'
# 		verbose_name_plural = 'Cardiopathy Fenotypes'

# 	def __str__(self):
# 		return self.name


#################### PATHO FENOTYPES ####################

# class Patho_Fenotypes(models.Model):
# 	"""
# 	A single pathology fenotype.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'Pathology Fenotype'
# 		verbose_name_plural = 'Pathology Fenotypes'

# 	def __str__(self):
# 		return self.name	


#################### TEST TYPE ####################
# N.B. Possible options are "NGS", "Mutuna", "OTHER"
# class TestType(models.Model):
# 	"""
# 	A single TestType.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'TestType'
# 		verbose_name_plural = 'TestTypes'

# 	def __str__(self):
# 		return self.name


#################### SAMPLE TYPE ####################
# N.B. Possible options are "Blood", "DNA", "OTHER"
# class SampleType(models.Model):
# 	"""
# 	A single SampleType.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'SampleType'
# 		verbose_name_plural = 'SampleTypes'

# 	def __str__(self):
# 		return self.name


#################### PROCESSING TYPE ####################
# N.B. Possible options are "OSR", "IMTC", "OTHER"
# class ProcessingType(models.Model):
# 	"""
# 	A single ProcessingType.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'ProcessingType'
# 		verbose_name_plural = 'ProcessingTypes'

# 	def __str__(self):
# 		return self.name
	

#################### GENES ####################
class Gene(models.Model):
	"""
	A single gene.
	"""
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Gene'
		verbose_name_plural = 'Genes'

	def __str__(self):
		return self.name
	

#################### MUTATIONS ####################
class Mutation(models.Model):
	"""
	A single mutation.
	"""
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Mutation'
		verbose_name_plural = 'Mutations'

	def __str__(self):
		return self.name
	

#################### AMINOACID CHANGES ####################
#class Aminoacidchange(models.Model):
#	"""
#	A single aminoacid change.
#	"""
#	name = models.CharField(max_length=100, unique=True)
#
#	class Meta:
#		ordering = ['name']
#		verbose_name = 'Aminoacidchange'
#		verbose_name_plural = 'Aminoacidchanges'
#
#	def __str__(self):
#		return self.name


#################### ACMG ####################

# class ACMG(models.Model):
# 	"""
# 	A single class.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'ACMG'
# 		verbose_name_plural = 'ACMGs'

# 	def __str__(self):
# 		return self.name


#################### Cromo anomalities ####################

# class Cromo_anomality(models.Model):
# 	"""
# 	A single class.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'Cromo anomality'
# 		verbose_name_plural = 'Cromo anomalities'

# 	def __str__(self):
# 		return self.name
	

#################### Eredity ####################

# class Eredity(models.Model):
# 	"""
# 	A single class.
# 	"""
# 	name = models.CharField(max_length=100, unique=True)

# 	class Meta:
# 		ordering = ['name']
# 		verbose_name = 'Eredity'
# 		verbose_name_plural = 'Eredities'

# 	def __str__(self):
# 		return self.name


#################### DOCTORS ####################

class Doctors(models.Model):
	"""
	A single cardiopathy fenotype.
	"""
	name = models.CharField(max_length=100, blank=False)
	surname = models.CharField(max_length=100, blank=False)

	class Meta:
		ordering = ['name']
		verbose_name = 'Doctor'
		verbose_name_plural = 'Doctors'

	def __str__(self):
		return self.name



###############################################################################
################################### GENETICS ##################################
###############################################################################
### \\\ It should contain a model for each type of exam:
### \\\ - Genetic profile
### \\\ - Genetic status
### \\\ - Genetic sample --> from each sample we can proceed with multiple tests!
### \\\ - Genetic tests
class Genetics(models.Model):
	
	patient = models.ForeignKey(
		"PatientProfile",
		on_delete=models.CASCADE,
	)

	# mi serve ancora?
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)

	class Meta:
		abstract = True # Tell django this is an abstract class, no table will be created

class Genetic_profile(Genetics):

	FIN_progressive_genetics = models.PositiveIntegerField(null=True, blank=True)
	FIN_number = models.CharField(max_length=100)
	PIN_number = models.CharField(max_length=100)
	class Meta:
		verbose_name = 'Genetic profile'
		verbose_name_plural = 'Genetic profiles'

class Genetic_status(Genetics):

	class Patient_status(models.TextChoices):
		P = "Proband", "Proband"
		F = "Familiar", "Familiar"	
	patient_status = models.CharField(
		max_length=100,
		choices=Patient_status,
		default=''
	)
	class proband_family_degree(models.TextChoices):
		Mo = "Mother", "Mother"
		Fa = "Father", "Father"
		GF = "Grand-father", "Grand-father"	
		GM = "Grand-mother", "Grand-mother"
	proband_familiarity = models.CharField(
		max_length=100,
		choices=proband_family_degree,
		default=''
	)

	class FamiliarityType(models.TextChoices):
		SD = "SD", "SD"
		C = "Cardiopathy", "Cardiopathy"	
		O = "Other pathologies", "Other pathologies"
	familiarityType = models.CharField(
		max_length=100,
		choices=FamiliarityType,
		default=''
	)
	cardio_fenotypes = models.CharField(max_length=100, null=True, default='')
	pato_fenotypes = models.CharField(max_length=100, null=True, default='')
	
	family_members = models.PositiveIntegerField(null=True, blank=True)
	class family_degree(models.TextChoices):
		Mo = "Mother", "Mother"
		Fa = "Father", "Father"
		GF = "Grand-father", "Grand-father"	
		GM = "Grand-mother", "Grand-mother"
	family_degree = models.CharField(
		max_length=100,
		choices=family_degree,
		default=''
	)

	children = models.PositiveIntegerField(null=True, blank=True)
	class Meta:
		verbose_name = 'Genetic status'
		verbose_name_plural = 'Genetic status'

## NO CONNECTION TO OTHER TABLES
class Genetic_sample(Genetics):
	
	# !!! it must have an ID !!!
	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
	)

	blood_sample_date = models.DateField()
	class Meta:
		verbose_name = 'Genetic sample'
		verbose_name_plural = 'Genetic samples'


class Genetic_test(Genetics):

	Consent_date = models.DateField()
	# !!! age at the moment of consent: do we need it? !!!
	
	class processing_Type(models.TextChoices):
		OSR = "OSR", "OSR"
		IMTC = "IMTC", "IMTC"
	processingType = models.CharField(
		max_length=100,
		choices=processing_Type,
		default=''
	)
	class test_Type(models.TextChoices):
		NGS = "NGS", "NGS"
		Mutuna = "Mutuna", "Mutuna"
	testType = models.CharField(
		max_length=100,
		choices=test_Type,
		default=''
	)


	########## !!! Only if "NGS" is selected, these should be compiled !!! ############
	class TestCategory(models.TextChoices):
		On = "Oncology", "Oncology"
		ChAr = "Channellopathies / Arrhythmias", "Channellopathies / Arrhythmias"
		Ca = "Cardiomiopathies", "Cardiomiopathies" 
		ND = "Neuromuscolar dystrophies"
		Col = "Collagenopathies", "Collagenopathies"
		Coa = "Coagulopathies", "Coagulopathies"
		SyDys = "Syndromes / Dysmorphisms", "Syndromes / Dysmorphisms"
		Me = "Metabolic", "Metabolic" 
		Sc = "Screening", "Screening"
		BrK = "Breast K", "Breast K"
		Nep = "Nephropathy", "Nephropathy"
		Neu = "Neuropathy", "Neuropathy"
		He = "Hematopathy", "Hematopathy"
	test_category = models.CharField(
		max_length=100,
		choices=TestCategory,
		default=''
	)

	# !!! Only if "Cannelopathies" is selected, these should be compiled !!!
	class ChanSubCategory(models.TextChoices):
		LQTS = "LQTS", "LQTS"
		ERS = "ERS", "ERS"
		JWS = "JWS", "JWS"
		Git = "Gitelman", "Gitelman"
		WPW = "WPW", "WPW"
		BAV = "BAV", "BAV" 
		BBB = "BBB", "BBB"
		CPVT = "CPVT", "CPVT"
		AF = "AF", "AF"
		BrS = "BrS", "BrS"
	chan_subcategory = models.CharField(
		max_length=100,
		choices=ChanSubCategory,
		default=''
	)

	# !!! Only if "Cardiomiopathies" is selected, these should be compiled !!!
	class CardSubCategory(models.TextChoices):
		HMC = "HMC", "HMC"
		ARVD = "ARVD", "ARVD"
		NCM = "NCM", "NCM"
		CMIO = "CMIO DILATED", "CMIO DILATED"
		Stru = "Stuctural", "Structural"
		Amilo = "Amilo", "Amilo" 
		Osi = "Osi", "Osi"
		Fab = "Fabry", "Fabry"
		ARVC = "ARVC", "ARVC"
		Guch = "Guch", "Guch"
	card_subcategory = models.CharField(
		max_length=100,
		choices=CardSubCategory,
		default=''
	)

	# !!! Only if "Collagenopathies" is selected, these should be compiled !!!
	class CollSubCategory(models.TextChoices):
		Ma = "Marfan", "Marfan"
		Eb = "Ebstein", "Ebstein"
		EhDa = "Ehler-danlos", "Ehler-danlos"
		AoAn = "Aorta Aneurysm", "Aorta Aneurysm"
	coll_subcategory = models.CharField(
		max_length=100,
		choices=CollSubCategory,
		default=''
	)

	# !!! Only if "Syndromes / Dysmorphisms" is selected, these should be compiled !!!
	class DysSubCategory(models.TextChoices):
		No = "Noonan", "Noonan"
		Tu = "Turner", "Turner"
		Kl = "Klinefelter", "Klinefelter"
	dys_subcategory = models.CharField(
		max_length=100,
		choices=DysSubCategory,
		default=''
	)

	# !!! Only if "Coagulopathies" is selected, these should be compiled !!!
	class CollSubCategory(models.TextChoices):
		II = "Factor II", "MFactor II"
		V = "Factor V", "Factor V"
		Thr = "Thrombophilia", "Thrombophilia"
		MTHFR = "MTHFR", "MTHFR"
		He = "Hemophilia", "Hemophilia"
		VaWi = "Van Willebrandt", "Van Willebrandt" 
	coll_subcategory = models.CharField(
		max_length=100,
		choices=CollSubCategory,
		default=''
	)
	

	# !!! Only if "Neuromuscolar dystrophies" is selected, these should be compiled !!!
	class NeuroSubCategory(models.TextChoices):
		St = "Steinert", "Steinert"
		Ata = "Ataxia", "Ataxia"
		Hun = "Huntington", "Huntington"
		ScaHu = "Scapulus humeral", "Scapulus humeral"
		Epi = "Epilepsy", "Epilepsy"
		ChaMaTo = "Charcot-Marie Tooth", "Charcot-Marie Tooth"
		LGMD = "LGMD", "LGMD"
	neuro_subcategory = models.CharField(
		max_length=100,
		choices=NeuroSubCategory,
		default=''
	)


	# !!! Only if "Metabolic dystrophies" is selected, these should be compiled !!!
	class MetabolicSubCategory(models.TextChoices):
		Di = "Diabetes", "Diabetes"
		Mo = "Mody", "Mody"
		Dip = "Dislipidemia", "Dislipidemia"
		MetAc = "Metal accumulation", "Metal accumulation"
		Ala = "Alagille", "Alagille"
		Gau = "Gaucher", "Gaucher"
		Po = "Pompe", "Pompe"
	metabolic_subcategory = models.CharField(
		max_length=100,
		choices=MetabolicSubCategory,
		default=''
	)

	# !!! Only if "Oncology" is selected, these should be compiled !!!
	class OncoSubCategory(models.TextChoices):
		Br = "Breast", "Breast"
		Pa = "Pancreas", "Pancreas"
		Ov = "Ovary", "Ovary"
		Co = "Colon", "Metal accumulation"
		Th = "Thyroid", "Thyroid"
		NF1 = "NF1", "NF1"
		Me = "Melanoma", "Melanoma"
	onco_subcategory = models.CharField(
		max_length=100,
		choices=OncoSubCategory,
		default=''
	)



	class NGSTestResult(models.TextChoices):
		P = "P", "Positive"
		N = "N", "Negative"
		NC = "NC", "Not conclusive"	
	NGStest_result = models.CharField(
		max_length=100,
		choices=NGSTestResult,
		default=''
	)
	class geneType(models.TextChoices):
		P = "Clinical", "Clinical"
		N = "Incidental", "Incidental"
	gene_type = models.CharField(
		max_length=100,
		choices=geneType,
		default=''
	)
	genes = models.ManyToManyField(
		Gene,
		blank=True,
		related_name='genes',
		help_text='Gene of this test.'
	)
	var_p = models.ManyToManyField(
		Mutation,
		blank=True,
		related_name='v1p',
		help_text='v1p'
	)
	var_c = models.ManyToManyField(
		Mutation,
		blank=True,
		related_name='v1c',
		help_text='v1c'
	)
	class Zygosity(models.TextChoices):
		HZ = "HZ", "HZ"
		OZ = "OZ", "OZ"
		HA = "HA", "HA"
	zygosity = models.CharField(
		max_length=100,
		choices=Zygosity,
		default=''
	)
	
	########## !!! Only if "Mutuna" is selected, these should be compiled !!! ############
	class ACMG(models.TextChoices):
		I = "I", "I"
		II = "II", "II"
		III = "III", "III"
		IV = "IV", "IV"
		V = "V", "V"
	ACMG = models.CharField(
		max_length=100,
		choices=ACMG,
		default=''
	)

	class MutunaTestResult(models.TextChoices):
		P = "Positive", "Positive"
		N = "Negative", "Negative"
		NC = "Not concluded", "Not concluded"	
	Mutunatest_result = models.CharField(
		max_length=100,
		choices=MutunaTestResult,
		default=''
	)
	class geneType(models.TextChoices):
		P = "Clinical", "Clinical"
		N = "Incidental", "Incidental"
	gene_type = models.CharField(
		max_length=100,
		choices=geneType,
		default=''
	)
	genes = models.ManyToManyField(
		Gene,
		blank=True,
		related_name='genes',
		help_text='Gene of this test.'
	)
	var_p = models.ManyToManyField(
		Mutation,
		blank=True,
		related_name='v1p',
		help_text='v1p'
	)
	var_c = models.ManyToManyField(
		Mutation,
		blank=True,
		related_name='v1c',
		help_text='v1c'
	)
	class Zygosity(models.TextChoices):
		HZ = "HZ", "HZ"
		OZ = "OZ", "OZ"
		HA = "HA", "HA"
	zygosity = models.CharField(
		max_length=100,
		choices=Zygosity,
		default=''
	)



########## !!! Only if "IMTC" is selected, these should be compiled !!! ############
	class sample_Type(models.TextChoices):
		B = "blood", "blood"
		D = "DNA", "DNA"
	sampleType = models.CharField(
		max_length=100,
		choices=sample_Type,
		default=''
	)
	aliquota = models.PositiveIntegerField(null=True, blank=True)

	class corsaNGS(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"	
	corsa_NGS = models.CharField(
		max_length=3,
		choices=corsaNGS,
		default=''
	)

	corsa_name = models.CharField(max_length=100, default='')

	editing_doctor = models.ManyToManyField(
		Doctors,
		blank=True,
		related_name='Editing_doctor'
	)


	class Sangen(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
	sangen = models.CharField(
		max_length=100,
		choices=Sangen,
		default=''
	)
	class SangenResult(models.TextChoices):
		P = "Positive", "Positive"
		N = "Negative", "Negative"
		NC = "Not concluded", "Not concluded"	
	Sangen_result = models.CharField(
		max_length=100,
		choices=SangenResult,
		default=''
	)

	class Reported(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
	reported = models.CharField(
		max_length=100,
		choices=Reported,
		default=''
	)
	report_data = models.DateField()

	reporting_doctor = models.ManyToManyField(
		Doctors,
		blank=True,
		related_name='Reporting_doctor'
	)



########## !!! Only if "OTHER" is selected, these should be compiled !!! ############

	eredity =  models.CharField(max_length=100, default='', blank=True)
	cromo_anomality =  models.CharField(max_length=100, default='', blank=True)
	class Meta:
		verbose_name = 'Genetic test'
		verbose_name_plural = 'Genetic tests'
