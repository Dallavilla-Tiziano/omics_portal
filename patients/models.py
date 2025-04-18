# IMPORT LIBRARIES
import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

# Salve

# "Patient" eredita da "models.Model", quindi sarà mappato in una tabella del database.
class Patient(models.Model):
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
	class Patient_type(models.TextChoices):
		PROBAND = "P", "Proband"
		RELATIVE = "R", "Relative"
            
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
	cardioref_id = models.CharField(max_length=100, blank=True, default='')
    
	patient_type = models.CharField(
		max_length=1,
		choices=Patient_type,
		blank=True,
		default=''
		)
    
    # Campo numerico positivo opzionale. null=True consente di avere valori nulli nel database.
	fin = models.PositiveIntegerField(null=True, blank=True)

	class Meta:
        # permissions: aggiunge un permesso personalizzato che potrà essere usato per controllare l’accesso a dati sensibili.
		permissions = [
		("access_sensible_info", "Can view patient sensible info")
		]

	def __str__(self):
		return f'{self.id}'

    # Restituisce l’URL alla vista patient_detail, utile nei template per fare link diretti all’oggetto.
	def get_absolute_url(self):
		return reverse("patient_detail", args=[str(self.id)])

class Sample(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # UUID come identificatore unico.
    # internal_id: identificativo leggibile o esterno del campione.
    internal_id = models.CharField(max_length=100)

    # ForeignKey: relazione uno-a-molti (un paziente → molti campioni).
    patient = models.ForeignKey(
        "Patient",
        # on_delete=models.CASCADE: se il paziente viene cancellato, anche i suoi campioni vengono eliminati.
        on_delete=models.CASCADE,
        # related_name="samples": permette di accedere ai campioni da un paziente usando patient.samples.
        related_name="samples"
    )

    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    collection_date = models.DateField()

    # Indica l’utente che ha raccolto il campione.
    collected_by = models.ForeignKey(
        get_user_model(),
        # Se l’utente viene cancellato, il campo diventa NULL.
        on_delete=models.SET_NULL,
        null=True    
    )

    storage_temperature = models.FloatField(
        help_text="Temperature in Celsius"
    )

    freezer_location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Storage freezer/box location"
    )

    initial_volume_ml = models.FloatField(
        help_text="Initial volume in milliliters"
    )

    remaining_volume_ml = models.FloatField(
        help_text="Remaining volume in milliliters",
        blank=True,
        null=True
    )

    class SampleStatus(models.TextChoices):
        STORED = "ST", "Stored"
        IN_USE = "IN", "In Use"
        EXHAUSTED = "EX", "Exhausted"
        CONTAMINATED = "CO", "Contaminated"
        DISPOSED = "DI", "Disposed"
        RETURNED = "RT", "Returned"

    status = models.CharField(
        max_length=2,
        choices=SampleStatus,
        default=SampleStatus.STORED
    )

    class SampleQuality(models.TextChoices):
        EXCELLENT = "EX", "Excellent"
        GOOD = "GD", "Good"
        FAIR = "FR", "Fair"
        POOR = "PR", "Poor"

    quality = models.CharField(
        max_length=2,
        choices=SampleQuality,
        default=SampleQuality.GOOD
    )

    def __str__(self):
        return f"{self.internal_id}"

class Analysis(models.Model):
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

    performed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        help_text="User who performed the analysis"
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
    
    # Patient ↔ (1:n) ↔ Sample
    # Sample ↔ (n:m) ↔ Analysis