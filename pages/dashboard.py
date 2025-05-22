from admin_tools.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
	columns = 2

	def init_with_context(self, context):

		self.children.append(modules.Group(
			title='Applications',
			display='tabs',
			children=[
				modules.Group(
					title='Kokoro',
					display='stacked',
					children=[
						modules.ModelList(
							title='Patient Profile',
							models=[
								'kokoro.models.PatientProfile',
								'kokoro.models.Study',
							],
						),
						modules.ModelList(
							title='Clinical Status',
							models=[
								'kokoro.models.Clinical_evaluation',
								'kokoro.models.Comorbidities',
								'kokoro.models.ClinicalEvent',
								'kokoro.models.Riskfactors',
								'kokoro.models.Cardiomiopathies',
								'kokoro.models.ClinicalEvent',
							],
						),
						modules.ModelList(
							title='Diagnostic Exams',
							models=[
								'kokoro.models.ECG',
								'kokoro.models.RMN_TC_PH',
								'kokoro.models.ECHO',
								'kokoro.models.late_potentials',
							],
						),
						modules.ModelList(
							title='Therapies',
							models=[
								'kokoro.models.Therapy',
							],
						),
						modules.ModelList(
							title='Procedures',
							models=[
								'kokoro.models.Ablation',
								'kokoro.models.DeviceImplant',
								'kokoro.models.CoronaryIntervention',
								'kokoro.models.ValveIntervention',
							],
						),
						modules.ModelList(
							title='Implanted Devices',
							models=[
								'kokoro.models.DeviceType',
								'kokoro.models.DeviceInstance',
								'kokoro.models.DeviceEvent',
								'kokoro.models.ValveIntervention',
							],
						),
						modules.ModelList(
							title='IMTC samples',
							models=[
								'kokoro.models.Sample',
							],
						),
						modules.ModelList(
							title='IMTC analysis',
							models=[
								'kokoro.models.ResearchAnalysis',
							],
						),
						modules.ModelList(
							title='Genetics',
							models=[
								'kokoro.models.Genetic_status',
								'kokoro.models.Genetic_test',
								'kokoro.models.Genetic_profile',
								'kokoro.models.ValveIntervention',
							],
						),
						modules.ModelList(
							title='Provocative test',
							models=[
								'kokoro.models.Ajmaline_test',
								'kokoro.models.Adrenaline_test',
								'kokoro.models.Flecainide_test',
								'kokoro.models.EP_study',
							],
						),
						modules.ModelList(
							title='Miscellaneous',
							models=[
								'kokoro.models.Symptoms',
								'kokoro.models.Gene',
								'kokoro.models.Mutation',
								'kokoro.models.Doctors',
							],
						),
					]
				),
				modules.ModelList(
					title='User Accounts',
					models=[
						'accounts.models.CustomUser',
					]
				),
			]
		))

		self.children.append(modules.AppList(
			title='Other Applications',
			exclude=[
				'django.contrib.*',
				'patients.models.*',
				'kokoro.models.*',
				'accounts.models.*',
			]
		))

		self.children.append(modules.AppList(
			title='Admin Tools',
			models=['django.contrib.*'],
		))
