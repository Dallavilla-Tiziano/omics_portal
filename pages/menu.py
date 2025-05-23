from admin_tools.menu import items, Menu

class CustomMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children += [
            items.MenuItem('Dashboard', '/admin/'),

            items.MenuItem(
                title='Kokoro',
                children=[
                    items.MenuItem('Patient Profile', children=[
                        items.ModelList('', models=[
                            'kokoro.models.PatientProfile',
                            'kokoro.models.Study',
                        ])
                    ]),
                    items.MenuItem('Clinical Status', children=[
                        items.ModelList('', models=[
                            'kokoro.models.Clinical_evaluation',
                            'kokoro.models.Comorbidities',
                            'kokoro.models.ClinicalEvent',
                            'kokoro.models.Riskfactors',
                            'kokoro.models.Cardiomiopathies',
                        ])
                    ]),
                    items.MenuItem('Diagnostic Exams', children=[
                        items.ModelList('', models=[
                            'kokoro.models.ECG',
                            'kokoro.models.RMN_TC_PH',
                            'kokoro.models.ECHO',
                            'kokoro.models.late_potentials',
                        ])
                    ]),
                    items.MenuItem('Therapies', children=[
                        items.ModelList('', models=['kokoro.models.Therapy'])
                    ]),
                    items.MenuItem('Procedures', children=[
                        items.ModelList('', models=[
                            'kokoro.models.Ablation',
                            'kokoro.models.DeviceImplant',
                            'kokoro.models.CoronaryIntervention',
                            'kokoro.models.ValveIntervention',
                        ])
                    ]),
                    items.MenuItem('Implanted Devices', children=[
                        items.ModelList('', models=[
                            'kokoro.models.DeviceType',
                            'kokoro.models.DeviceInstance',
                            'kokoro.models.DeviceEvent',
                        ])
                    ]),
                    items.MenuItem('IMTC Samples', children=[
                        items.ModelList('', models=['kokoro.models.Sample'])
                    ]),
                    items.MenuItem('IMTC Analysis', children=[
                        items.ModelList('', models=['kokoro.models.ResearchAnalysis'])
                    ]),
                    items.MenuItem('Genetics', children=[
                        items.ModelList('', models=[
                            'kokoro.models.Genetic_status',
                            'kokoro.models.Genetic_test',
                            'kokoro.models.Genetic_profile',
                        ])
                    ]),
                    items.MenuItem('Provocative Test', children=[
                        items.ModelList('', models=[
                            'kokoro.models.Ajmaline_test',
                            'kokoro.models.Adrenaline_test',
                            'kokoro.models.Flecainide_test',
                            'kokoro.models.EP_study',
                        ])
                    ]),
                    items.MenuItem('Miscellaneous', children=[
                        items.ModelList('', models=[
                            'kokoro.models.Symptoms',
                            'kokoro.models.Gene',
                            'kokoro.models.Mutation',
                            'kokoro.models.Doctors',
                        ])
                    ]),
                ]
            ),

            items.AppList(
                title='Patients',
                models=['patients.models.*']
            ),

            items.AppList(
                title='Accounts',
                models=['accounts.models.*']
            ),

            items.AppList(
                title='Other Applications',
                exclude=[
                    'django.contrib.*',
                    'kokoro.models.*',
                    'patients.models.*',
                    'accounts.models.*',
                ]
            ),

            items.AppList(
                title='Admin Tools',
                models=['django.contrib.*']
            ),

            items.MenuItem('Documentation', 'https://docs.djangoproject.com/en/stable/'),
        ]
