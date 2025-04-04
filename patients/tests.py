# patients/tests.py
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient, Sample, Analysis
from patients.views import PatientListView
from django.http import HttpRequest
from patients.query_helpers import get_filtered_patients

User = get_user_model()

class TestQueryHelpers(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create(username="testuser")
		
		self.patient1 = Patient.objects.create(
			last_name="Smith",
			first_name="John",
			sex="M",
			date_of_birth="1980-01-01",
			nation="Italy",
			patient_type="P"
		)
		self.patient2 = Patient.objects.create(
			last_name="Doe",
			first_name="Jane",
			sex="F",
			date_of_birth="1990-01-01",
			nation="France",
			patient_type="P"
		)

		self.sample1 = Sample.objects.create(
			internal_id="S1",
			patient=self.patient1,
			type="Peripheral Blood",
			location="Lab A",
			collection_date="2020-01-01",
			collected_by=self.user,
			storage_temperature=4.0,
			freezer_location="Freezer 1",
			initial_volume_ml=10.0,
			remaining_volume_ml=5.0,
			status="ST",
			quality="GD"
		)
		self.analysis1 = Analysis.objects.create(
			analysis_name="Analysis 1",
			type="WES",
			performed_by=self.user
		)
		self.analysis1.samples.add(self.sample1)

		self.sample2 = Sample.objects.create(
			internal_id="S2",
			patient=self.patient2,
			type="Other Type",
			location="Lab B",
			collection_date="2020-01-02",
			collected_by=self.user,
			storage_temperature=4.0,
			freezer_location="Freezer 2",
			initial_volume_ml=10.0,
			remaining_volume_ml=5.0,
			status="ST",
			quality="GD"
		)
		self.analysis2 = Analysis.objects.create(
			analysis_name="Analysis 2",
			type="RNAseq",
			performed_by=self.user
		)
		self.analysis2.samples.add(self.sample2)

	def test_no_filters_returns_all_patients(self):
		request = self.factory.get("/patients/")
		qs = get_filtered_patients(request)
		self.assertEqual(qs.count(), 2)

	def test_filter_by_sample_and_analysis(self):
		request = self.factory.get("/patients/", data={
			"sample_type": "Peripheral Blood",  # Now for SampleFilter.
			"status": "ST",                       # Still for SampleFilter.
			"analysis_type": "WES",               # Now for AnalysisFilter.
			"performed_by": self.user.id,         # AnalysisFilter.
		})
		qs = get_filtered_patients(request)
		self.assertEqual(qs.count(), 1)
		self.assertEqual(qs.first(), self.patient1)

	def test_filter_no_results(self):
		request = self.factory.get("/patients/", data={
			"sample_type": "Nonexistent Type",  # Use new key.
		})
		qs = get_filtered_patients(request)
		self.assertEqual(qs.count(), 0)

class TestPatientListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="testuser")
        
        # Create two patients.
        self.patient1 = Patient.objects.create(
            last_name="Smith",
            first_name="John",
            sex="M",
            date_of_birth="1980-01-01",
            nation="Italy",
            patient_type="P"
        )
        self.patient2 = Patient.objects.create(
            last_name="Doe",
            first_name="Jane",
            sex="F",
            date_of_birth="1990-01-01",
            nation="France",
            patient_type="P"
        )
        
        # Create a sample for patient1 that meets filter criteria.
        self.sample1 = Sample.objects.create(
            internal_id="S1",
            patient=self.patient1,
            type="Peripheral Blood",
            location="Lab A",
            collection_date="2020-01-01",
            collected_by=self.user,
            storage_temperature=4.0,
            freezer_location="Freezer1",
            initial_volume_ml=10.0,
            remaining_volume_ml=5.0,
            status="ST",
            quality="GD"
        )
        self.analysis1 = Analysis.objects.create(
            analysis_name="Analysis 1",
            type="WES",
            performed_by=self.user
        )
        self.analysis1.samples.add(self.sample1)
        
        # Create a sample for patient2 that does NOT meet the filtering criteria.
        self.sample2 = Sample.objects.create(
            internal_id="S2",
            patient=self.patient2,
            type="Other Type",
            location="Lab B",
            collection_date="2020-01-02",
            collected_by=self.user,
            storage_temperature=4.0,
            freezer_location="Freezer2",
            initial_volume_ml=10.0,
            remaining_volume_ml=5.0,
            status="ST",
            quality="GD"
        )
        self.analysis2 = Analysis.objects.create(
            analysis_name="Analysis 2",
            type="RNAseq",
            performed_by=self.user
        )
        self.analysis2.samples.add(self.sample2)

    def test_view_no_filters(self):
        url = reverse("patient_list")  # Ensure your URL pattern is named 'patient_list'
        request = self.factory.get(url)
        request.user = self.user
        response = PatientListView.as_view()(request)
        table = response.context_data["table"]
        self.assertEqual(len(table.page.object_list), 2)

    def test_view_with_valid_filters(self):
        url = reverse("patient_list")
        request = self.factory.get(url, data={
            "sample_type": "Peripheral Blood",
            "status": "ST",
            "analysis_type": "WES",
            "performed_by": self.user.id,
        })
        request.user = self.user
        response = PatientListView.as_view()(request)
        table = response.context_data["table"]
        self.assertEqual(len(table.page.object_list), 1)
        self.assertEqual(table.page.object_list[0].record, self.patient1)

    def test_view_with_invalid_filters(self):
        url = reverse("patient_list")
        request = self.factory.get(url, data={
            "sample_type": "Nonexistent Type",
        })
        request.user = self.user
        response = PatientListView.as_view()(request)
        table = response.context_data["table"]
        self.assertEqual(len(table.page.object_list), 0)