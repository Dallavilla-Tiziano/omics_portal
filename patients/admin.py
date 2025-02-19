from django.contrib import admin
from .models import Patient, Data

class DataInline(admin.TabularInline):
	model = Data

class PatientAdmin(admin.ModelAdmin):
	inlines = [
		DataInline,
	]
	list_display = ("last_name", "first_name", "sex", "date_of_birth")

admin.site.register(Patient, PatientAdmin)