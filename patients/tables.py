import django_tables2 as tables
from .models import Patient
from django.utils.html import format_html
from django.urls import reverse

class PatientTable(tables.Table):
    patient_type = tables.TemplateColumn("{{ record.patient_type }}", verbose_name="Status")
    sex = tables.TemplateColumn("{{ record.sex }}", verbose_name="Sex")

    # Add an empty column to populate with an icon that send the user to the detail page
    details = tables.Column(empty_values=(), verbose_name="Details")
    def render_details(self, record):
        """ Renders an icon that links to the patient's detail page """
        url = reverse("patient_detail", args=[record.pk])
        return format_html('<a href="{}" class="text-primary"><i class="bi bi-eye"></i></a>', url)

    class Meta:
        model = Patient
        fields = ("last_name", "first_name", "date_of_birth", "sex", "patient_type", "fin", "nation")

        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-hover table-responsive"
            }