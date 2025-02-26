import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Patient(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False
		)
	class Sex(models.TextChoices):
		MAN = "M", "Male"
		WOMAN = "F", "Female"
	class Patient_type(models.TextChoices):
		PROBAND = "P", "Proband"
		RELATIVE = "R", "Relative"
	last_name = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
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
	fin = models.PositiveIntegerField(null=True, blank=True)

	class Meta:
		permissions = [
		("access_sensible_info", "Can view patient sensible info")
		]

	def __str__(self):
		return self.last_name

	def get_absolute_url(self):
		return reverse("patient_detail", args=[str(self.id)])

class Data(models.Model):
	patient = models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name="data",
		)

	type = models.CharField(max_length=100)
	location = models.CharField(max_length=100)

	def __str__(self):
		return self.type