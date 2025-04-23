from django.db import models
import uuid
import datetime
from dateutil.relativedelta import relativedelta

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

class Sample(models.Model):
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
    collection_date = models.DateField(
        # sample_collection_date in canva
    )
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
        blank=True,  # Optional notes
    )

    def __str__(self):
        return f"{self.imtc_id} ({self.get_procedure_type_display()})"