from django.contrib import admin
from .models import PatientProfile, Sample, DeviceType, DeviceInstance, DeviceEvent, Ablation, DeviceImplant


class AblationAdmin(admin.ModelAdmin):
		list_display = ("date", "total_area", "total_rf_time")
class AblationtInline(admin.TabularInline):
	model = Ablation
	extra = 1
class DeviceImplantAdmin(admin.ModelAdmin):
		list_display = ("date", "lv4_ring", "lv3_ring", "lv2_ring", "lv1_tip")
class DeviceImplantInline(admin.TabularInline):
	model = DeviceImplant
	extra = 1
class DeviceEventAdmin(admin.ModelAdmin):
		list_display = ("timestamp", "date", "inappropriate_pre_rf_shock_cause", "inappropriate_post_brs_shock_cause")
class DeviceEventInline(admin.TabularInline):
	model = DeviceEvent
	extra = 1

class DeviceTypeAdmin(admin.ModelAdmin):
		list_display = ("Model", "Design", "Company")

class DeviceInstanceAdmin(admin.ModelAdmin):#
	inlines = [
		DeviceEventInline,
	]
	list_display = ("device_type", "serial_number", "implantation")
class DeviceInstanceInline(admin.TabularInline):
	model = DeviceInstance
	extra = 1

class SampleAdmin(admin.ModelAdmin):
	list_display = ("imtc_id", "patient", "procedure_type", "collection_date")
class SampleInline(admin.TabularInline):
	model = Sample
	extra = 1

class PatientProfileAdmin(admin.ModelAdmin):
	inlines = [
		SampleInline,
		AblationtInline,
		DeviceInstanceInline,
		DeviceImplantInline,
	]
	# "list_display": definisce le colonne visibili nella lista pazienti. Mostra cognome, nome, sesso e data di nascita.
	list_display = ("last_name", "first_name", "sex", "date_of_birth")

admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(DeviceInstance, DeviceInstanceAdmin)
admin.site.register(DeviceEvent, DeviceEventAdmin)
admin.site.register(Ablation, AblationAdmin)
admin.site.register(DeviceImplant, DeviceImplantAdmin)
admin.site.register(Sample, SampleAdmin)
