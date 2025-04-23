from django.db import models
import uuid
import datetime
from dateutil.relativedelta import relativedelta

## PATIENTS ##
# "Patient" eredita da "models.Model", quindi sarà mappato in una tabella del database.
class Patient_profile(models.Model):
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

	class Meta:
		# permissions: aggiunge un permesso personalizzato che potrà essere usato per controllare l’accesso a dati sensibili.
		permissions = [
		("access_sensible_info", "Can view patient sensible info")
		]

	def __str__(self):
		return f'{self.id}'

## DEVICES ##
class DeviceType(models.Model):

	id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

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
    # Manufacturer should be the same as company?
    # Dispositivo
    # Tipologiaare these needed?
    # Tipo di device has been joined with type above.


     
## PROCEDURES ##
# Procedures common fields are defined in a base class which is then inherited by single procedures
class ProcedureBase(models.Model):

    patient = models.ForeignKey(
        "Patient_profile",
        on_delete=models.CASCADE,
        related_name="samples",
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
	rf_w =  = models.FloatField(null=True, blank=True)

	complication = models.CharField(
        max_length=2,
        choices=Complication.choices,
        blank=True,
        default="",
    )

    complication_type = models.CharField(max_length=250)
    therapy = models.CharField(max_length=250)
    # REDO ABLAZIONE is not needed anymore

class Device_Implant(ProcedureBase):

	# CONDUCTION TIMES RV-PACED TO LV-SENSED
	lv4_ring = models.FloatField(null=True, blank=True)
	lv3_ring = models.FloatField(null=True, blank=True)
	lv2_ring = models.FloatField(null=True, blank=True)
	lv1_tip = models.FloatField(null=True, blank=True)
	# CONDUCTION TIMES RV-SENSED TO LV-SENSED
	# PACING CAPTURE THRESHOLD
	v =  models.FloatField(null=True, blank=True)
	ms = models.PositiveIntegerField(null=True, blank=True)
	lv_pulse_configuration_2_lv2 = models.FloatField(null=True, blank=True)
	pacing_impendance = models.FloatField(null=True, blank=True)
	# PACING CAPTURE THRESHOLD
	# Are these fieds (ms, V) repeated or are they needed, or this needs to be logged?

	#### shouldn't the implant be identified by an id?

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
        "Patient_profile",
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
