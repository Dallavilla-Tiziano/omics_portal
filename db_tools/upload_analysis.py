from patients.models import Patient, Sample, Analysis
from django.contrib.auth import get_user_model
import pandas as pd

# Load CSV file
analyses = pd.read_csv('/code/db_tools/analysis_imtc.csv', sep='\t')

# Get the User model
User = get_user_model()

success_count = 0
error_count = 0

# Open a log file to capture errors
with open("/code/db_tools/analysis_import_errors.log", "w") as log_file:
    for index, row in analyses.iterrows():
        try:
            # Retrieve the Sample instances (Assuming multiple sample IDs are separated by ";")
            sample_ids = row['samples'].split(";")
            samples = Sample.objects.filter(internal_id__in=sample_ids)

            if not samples.exists():
                log_file.write(f"Error: No valid samples found for Analysis in row {index}. Skipped.\n")
                error_count += 1
                continue

            # Retrieve the User instance for 'performed_by'
            performed_by = User.objects.filter(username=row.get('performed_by', 'imtc')).first()

            # Create Analysis instance
            analysis = Analysis.objects.create(
                analysis_name = row['Exp'],
                type = row['Tech'],
                performed_by = performed_by,  # Assign user or None
                result_files = row['results'] if pd.notna(row['results']) else None,
                date_performed = row['Data Corsa']
            )
            analysis.samples.set(samples)  # Link samples to the analysis
            # analysis.save()  # Save analysis
            success_count += 1

        except Exception as e:
            log_file.write(f"Unexpected error on row {index}: {str(e)}\n")
            error_count += 1

print(f"✅ Import finished: {success_count} analyses added, {error_count} errors.")
