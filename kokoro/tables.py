import django_tables2 as tables
from .models import PatientProfile
from django.utils.html import format_html
from django.urls import reverse

class BaseTable(tables.Table):
    """ Base table with common configurations """
    
    class Meta:
        abstract = True
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-hover table-bordered table-responsive rounded shadow-sm",
            "thead": {
                "class": "table-dark"
            }
        }

class PatientTable(BaseTable):
    details = tables.Column(empty_values=(), verbose_name="", orderable=False)

    def render_details(self, record):
        url = reverse("kokoro:patient_detail", args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-outline-primary"><i class="bi bi-eye-fill"></i></a>',
            url
        )

    class Meta(BaseTable.Meta):
        model = PatientProfile
        fields = ("id", "date_of_birth", "sex", "nation")
        sequence = ("...", "details")
