from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_in_future(value):
	if value and value > timezone.now().date():
		raise ValidationError("Date cannot be in the future.")
	return value

def clean_positive_float(value, label="Value"):
	if value in (None, ''):
		return None
	try:
		value = float(value)
	except ValueError:
		raise ValidationError(f"{label} must be a number.")
	if value < 0:
		raise ValidationError(f"{label} must be a positive float.")
	return value

def clean_positive_int(value, label="Value"):
	if value in (None, ''):
		return None
	try:
		value = int(value)
	except ValueError:
		raise ValidationError(f"{label} must be a number.")
	if value < 0:
		raise ValidationError(f"{label} must be a positive integer.")
	return value

def clean_start_end_date(value_start, value_end):
	if value_start and value_end and value_start > value_end:
		raise ValidationError("Start date can't be set after end date.")
	return value
