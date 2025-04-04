from django.contrib import admin
from .models import Patient, Sample, Analysis

class SampleInline(admin.TabularInline):
	model = Sample

class AnalysisInline(admin.TabularInline):
    model = Analysis.samples.through  # ManyToMany relationship needs `through`

class PatientAdmin(admin.ModelAdmin):
	inlines = [
		SampleInline,
	]
	list_display = ("last_name", "first_name", "sex", "date_of_birth")

class SampleAdmin(admin.ModelAdmin):
    inlines = [
        AnalysisInline,  # Show related analyses in Sample view
    ]
    list_display = ("internal_id", "type", "location", "collection_date", "status", "quality")

class AnalysisAdmin(admin.ModelAdmin):
    filter_horizontal = ("samples",)  # Allows better UI for ManyToMany fields
    list_display = ("type", "date_performed", "performed_by")

admin.site.register(Patient, PatientAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Analysis, AnalysisAdmin)