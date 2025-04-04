from patients.models import Patient, Sample
from django.contrib.auth import get_user_model
import pandas as pd

# Load CSV file
samples = pd.read_csv('/code/db_tools/odb_et_patient_psample.csv')

# Get the User model
User = get_user_model()

success_count = 0
error_count = 0

# Open a log file to capture errors
with open("/code/db_tools/sample_import_errors.log", "w") as log_file:
	for index, row in samples.iterrows():
		try:
			# Retrieve the Patient instance
			patient = Patient.objects.get(id=row['Patient uuid'])

			# Retrieve the User instance for 'collected_by'
			collected_by = User.objects.filter(username='imtc').first()

			# Create Sample instance
			sample = Sample(
				internal_id=row['Code_psample'],
				patient=patient,
				type=row['Primary Material Code'],
				location=row['Lab name'],
				collection_date=row['Collection Date'],
				collected_by=collected_by,  # Assign user or None
				storage_temperature=-80.0,
				freezer_location='',
				initial_volume_ml=100.0,
				remaining_volume_ml=100.0,
				status='ST',
				quality='GD'
			)

			sample.save()  # Save sample
			success_count += 1

		except Patient.DoesNotExist:
			log_file.write(f"Error: Patient with ID {row['Patient uuid']} does not exist. Row {index} skipped.\n")
			error_count += 1

		except Exception as e:
			log_file.write(f"Unexpected error on row {index}: {str(e)}\n")
			error_count += 1

print(f"✅ Import finished: {success_count} samples added, {error_count} errors.")
