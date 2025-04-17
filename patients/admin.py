# IMPORT
from django.contrib import admin
# Importa i modelli Patient, Sample e Analysis dal file models.py corrente (. indica la directory corrente). 
from .models import Patient, Sample, Analysis

# Serve per visualizzare i campi di Sample direttamente nella pagina di un altro modello, 
# # in formato tabellare (TabularInline).
# "model = Sample": dice che questa tabella verrà usata dentro "PatientAdmin", 
# cioè ogni paziente mostrerà direttamente i suoi campioni (sample) associati
class SampleInline(admin.TabularInline):
	model = Sample

# Anche questa è una TabularInline, ma riferita a una relazione ManyToMany.
# Analysis.samples.through: samples è presumibilmente un campo ManyToManyField nel modello Analysis, 
# e through è il modello di relazione intermedio che Django crea per gestire questa connessione. 
# Quando una relazione ManyToMany è esplicita o necessita di una gestione fine, 
# puoi accedere al modello intermedio con .through.
class AnalysisInline(admin.TabularInline):
    model = Analysis.samples.through  # ManyToMany relationship needs `through`

# Personalizza la pagina admin del modello Patient.
class PatientAdmin(admin.ModelAdmin):
    # "inlines": indica che nella pagina di ogni paziente vogliamo vedere e modificare i campioni associati (SampleInline).
	inlines = [
		SampleInline,
	]
    # "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")

class SampleAdmin(admin.ModelAdmin):
    inlines = [
        AnalysisInline,  # Show related analyses in Sample view
    ]
    list_display = ("internal_id", "type", "location", "collection_date", "status", "quality")

# Personalizza la visualizzazione di Analysis.
class AnalysisAdmin(admin.ModelAdmin):
    # filter_horizontal: migliora l'interfaccia utente per i campi ManyToMany, mostrando un widget con doppie liste selezionabili orizzontalmente.
    filter_horizontal = ("samples",)  # Allows better UI for ManyToMany fields
    # list_display: mostra tipo, data di esecuzione e chi ha eseguito l’analisi.
    list_display = ("type", "date_performed", "performed_by")

# Registra i tre modelli nel sito admin di Django, associandoli alle rispettive classi di personalizzazione. 
# Questo è fondamentale: senza questa riga i modelli non compaiono nel pannello.
admin.site.register(Patient, PatientAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Analysis, AnalysisAdmin)