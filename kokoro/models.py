from django.db import models
from django.core.exceptions import ValidationError
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
	
class Clinical_Status(models.Model):

    # mi serve ancora?
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)
	
# !!! Vorrei che Clinical_evaluation fosse una sottoclasse di Clinical_Status ma non so se
#     questa è la "sede giusta" / il codice appropiato per occuparsi di ciò  
class Clinical_evaluation(models.Model):

	# per ora va bene così, ma il formato di data che si vede è scomodissimo
	date_of_visit = models.DateField()

	class Symptoms(models.TextChoices):
		CA = "Cardiac arrest", "Cardiac arrest"
		P = "Palpitations", "Palpitations"
		A = "Asymptomatic", "Asymptomatic"
		O = "Other", "Other"
		
	symptoms = models.CharField(
		max_length=14,
		choices=Symptoms
	)
 
	spec_other_symptoms = models.CharField(max_length=100, blank=True, default='')

    # questo nasce dal desiderio di far comparire "spec_other_symptoms" solo se effettivamente
	# si seleziona "Other" a "symptoms"
	def clean(self):
		if self.symptoms == self.Symptoms.O and not self.spec_other_symptoms:
			raise ValidationError("You must specify 'Other' symptoms if 'Other' is selected.")

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

    