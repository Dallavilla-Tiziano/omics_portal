from django.db import models


# libreria necessaria per opzioni a scelte multiple... spoiler, dà errore!
#from multiselectfield import MultiSelectField

import uuid
import datetime
from dateutil.relativedelta import relativedelta

#################### THERAPIES ####################

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

#################### PATIENTS ####################
# "Patient" eredita da "models.Model", quindi sarà mappato in una tabella del database.

class Study(models.Model):

	name = models.CharField(max_length=100, unique=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name

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
	cardioref_id = models.CharField(max_length=100, blank=True, default='')

	therapies = models.ManyToManyField(
		Therapy,
		blank=True,
		related_name='patients',
		help_text='Therapies this patient is on.'
	)

	studies = models.ManyToManyField(
		Study,
		through='PatientStudy',
		related_name='participants',
		blank=True,
		help_text='Which studies this patient is enrolled in'
	)

	class Meta:
		# permissions: aggiunge un permesso personalizzato che potrà essere usato per controllare l’accesso a dati sensibili.
		permissions = [
		("access_sensible_info", "Can view patient sensible info")
		]

	def __str__(self):
		return f'{self.id}'

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

## PROCEDURES ##
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

	complication_type = models.CharField(max_length=250)
	therapy = models.CharField(max_length=250)
	# REDO ABLAZIONE is not needed anymore

class DeviceImplant(ProcedureBase):

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

## DEVICES ##
class DeviceType(models.Model):

	id = models.UUIDField(
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)
	class Design(models.TextChoices):
		SD_PACEMAKER = "Single\\Dual Pacemaker"
		SD_CHAMBER_ICD = "Single\\Dual Chamber ICD"
		OTHER = "Other"

	class Model(models.TextChoices):
		IN7F4IS4 = "INTICA 7 HF-TQPDF4/IS4"
		RI7HFQP = "RIVACOR 7 HF-T QP"
		IN7HFIS4 = "INTICA 7 HF-TQPDF1/IS4"
		INN7HFQP = "INTICA NEO 7 HF-T QP"

	class Type(models.TextChoices):
		CARDIAC_DEVICE = "CD", "Cardiac Device"
		LOOP_RECORDER = "LR", "Loop Recorder"
		PACE_MAKER = "PM", "Pace Maker"

	class Company(models.TextChoices):
		ABBOTT = "AB", "Abbott"
		BIOTRONIK = "BT", "Biotronik"
		MEDTRONIC = "MT", "Medtronic"
		BOSTON = "BS", "Boston"
		STJUDE = "SJ", "St. Jude"

	type = models.CharField(
		max_length=2,
		choices=Type.choices,
		blank=True,
		default="",
	)
	company = models.CharField(
		max_length=2,
		choices=Company.choices,
		blank=True,
		default="",
	)
	# Dispositivo, Tipologia are these needed?
	# Tipo di device has been joined with type above.
	model = models.CharField(
		max_length=50,
		choices=Model.choices,
		blank=True,
		default="",
	)
	design = models.CharField(
		max_length=50,
		choices=Design.choices,
		blank=True,
		default="",
		)# I'm calling it design because i can't find a more appropriate name rn

	def __str__(self):
		return f"{self.name} ({self.manufacturer})"

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

	implantation = models.OneToOneField(
		DeviceImplant,
		on_delete=models.CASCADE,
		related_name="device",
	)

	patient = models.ForeignKey(
		PatientProfile,
		on_delete=models.CASCADE,
		related_name="device",
	)
	def __str__(self):
		return f"{self.device_type.name} SN:{self.serial_number}"

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

	# Internal Date, potentially can be used to check if dat was inserted correctly
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
		return f"{self.get_event_type_display()} @ {self.timestamp:%Y-%m-%d %H:%M}"

## SAMPLES ##

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

	def __str__(self):
		return f"{self.imtc_id} ({self.get_procedure_type_display()})"
## IMTC ##
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
		verbose_name = "Analysis"
		verbose_name_plural = "Analyses"  # Fixes incorrect pluralization

	def __str__(self):
		return f"{self.get_type_display()} ({self.date_performed})"	

class Clinical_Status(models.Model):
	
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
	
# !!! Vorrei che Clinical_evaluation fosse una sottoclasse di Clinical_Status ma non so se
#     questa è la "sede giusta" / il codice appropiato per occuparsi di ciò  

class Clinical_evaluation(Clinical_Status):

	# per ora va bene così, ma il formato di data che si vede è scomodissimo
	date_of_visit = models.DateField()
	 
	### SYMPTOMS - TRIAL 1:
	###################################################################################
	# questo sarebbe andato bene se avessi voluto selezionare solo una voce alla volta,
	# ma io le voglio molteplicamente selezionabili!
	#class Symptoms(models.TextChoices):
	#	CA = "Cardiac arrest", "Cardiac arrest"
	#	S = "Syncope", "Syncope"
	#	P = "Palpitations", "Palpitations"
	#	A = "Asymptomatic", "Asymptomatic"
	#	O = "Other", "Other"
		
	#symptoms = models.CharField(
	#	max_length=14,
	#	choices=Symptoms
	#)
 
	#spec_other_symptoms = models.CharField(max_length=100, blank=True, default='')

	# questo nasce dal desiderio di far comparire "spec_other_symptoms" solo se effettivamente
	# si seleziona "Other" a "symptoms"
	#def clean(self):
	#	if self.symptoms == self.Symptoms.O and not self.spec_other_symptoms:
	#		raise ValidationError("You must specify 'Other' symptoms if 'Other' is selected.")
	#########################################################################################

	### SYMPTOMS - TRIAL 2:
	####################################################################
	#SYMPTOM_CHOICES = (
	#    ('CA', 'Cardiac arrest'),
	#    ('S', 'Syncope'),
	#    ('P', 'Palpitations'),
	#    ('A', 'Asymptomatic'),
	#    ('O', 'Other'),
	#)
	
	#symptoms = MultiSelectField(choices=SYMPTOM_CHOICES, max_length=20, blank=True)
	#spec_other_symptoms = models.CharField(max_length=100, blank=True, default='')
	
	#def clean(self):
	#	super().clean()  # mantiene pulizia generale
	#	if 'O' in self.symptoms and not self.spec_other_symptoms:
	#		raise ValidationError("You must specify 'Other' symptoms if 'Other' is selected.")
	##########################################################################################

	# ho messo solo queste opzioni perché sono le uniche attualmente esistenti,
	# ma credo che sarà opportuno inserirne altre
	class EVApreATC(models.TextChoices):
		VF = "VF", "Ventricular Fibrillation"
		VTNS = "VTNS", "Non-sustained ventricular tachycardia"
		VT = "VT", "Ventricular tachycardia" 
		VFNS = "VFNS", "Non-sustained ventricular fibrillation"

	EvaluationPreATC = models.CharField(
		max_length=38,
		choices=EVApreATC
	)

	# OPZIONE 1 per campo Yes/No
	SVT = models.BooleanField(
		default=False,
		verbose_name=" SVT (SopraVentricular Tachycardia)"  # Etichetta leggibile nei form/admin
	)

	# OPZIONE 2 per campo Yes/No
	class AF(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	atrial_fibrillation = models.CharField(
		max_length=3,
		choices=AF
	)

	class Flutter(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	flutter = models.CharField(
		max_length=3,
		choices=Flutter
	)

	class AT(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"

	atrial_tachycardia = models.CharField(
		max_length=3,
		choices=AT
	)

	class TPSV(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	paroxysmal_supraventricular_tachycardia = models.CharField(
		max_length=3,
		choices=TPSV
	)

	class WPW(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	wolff_parkinson_white = models.CharField(
		max_length=3,
		choices=WPW
	)

	class BESV(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	besv = models.CharField(
		max_length=3,
		choices=BESV
	)

	class BEV(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	bev = models.CharField(
		max_length=3,
		choices=BEV
	)

	class PVT(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	premature_ventricular_contraction = models.CharField(
		max_length=3,
		choices=PVT
	)

	class Thrombosis(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	thrombosis = models.CharField(
		max_length=3,
		choices=Thrombosis
	)

class Comorbidities(Clinical_Status):

	class Hyper(models.TextChoices):
		Y = "Yes", "Yes"
		N = "No", "No"
		
	arterial_hypertension = models.CharField(
		max_length=3,
		choices=Hyper
	)