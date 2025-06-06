# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AccountsCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'
        unique_together = (('user', 'email'), ('user', 'primary'),)


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AccountsCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts_customuser'


class AccountsCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_groups'
        unique_together = (('customuser', 'group'),)


class AccountsCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class KokoroAblation(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateField()
    total_area = models.FloatField(blank=True, null=True)
    bas_area_a_160 = models.FloatField(blank=True, null=True)
    bas_area_a_180 = models.FloatField(blank=True, null=True)
    bas_area_a_200 = models.FloatField(blank=True, null=True)
    basal_pdm = models.FloatField(blank=True, null=True)
    total_rf_time = models.FloatField(blank=True, null=True)
    rf_w = models.FloatField(blank=True, null=True)
    complication = models.CharField(max_length=2)
    complication_type = models.CharField(max_length=250)
    therapy = models.CharField(max_length=250)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_ablation'


class KokoroAdrenalineTest(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_provocative_test = models.DateField()
    adrenaline_dose = models.FloatField(blank=True, null=True)
    adrenaline_result = models.CharField(max_length=16)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_adrenaline_test'


class KokoroAjmalineTest(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_provocative_test = models.DateField()
    ajmaline_dose = models.FloatField(blank=True, null=True)
    ajmaline_dose_per_kg = models.FloatField(blank=True, null=True)
    ajmaline_result = models.CharField(max_length=16)
    induced_arrhythmia = models.CharField(max_length=5)
    bas_area_a_160 = models.FloatField(blank=True, null=True)
    bas_area_a_180 = models.FloatField(blank=True, null=True)
    bas_area_a_200 = models.FloatField(blank=True, null=True)
    bas_area_a_250 = models.FloatField(blank=True, null=True)
    bas_area_a_280_300 = models.FloatField(blank=True, null=True)
    pdm = models.FloatField(blank=True, null=True)
    brs_pattern = models.CharField(max_length=8)
    dose_to_positive_ecg = models.FloatField(blank=True, null=True)
    time_to_positive_ecg = models.DurationField(blank=True, null=True)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_ajmaline_test'


class KokoroCardiomiopathies(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_cardiomiopathies'


class KokoroClinicalEvaluation(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_visit = models.DateField()
    primary_cause_of_cd = models.CharField(db_column='Primary_Cause_of_CD', max_length=13)  # Field name made lowercase.
    specify_ischemic = models.CharField(max_length=100)
    mi_zone = models.CharField(max_length=100)
    specify_non_ischemic = models.CharField(max_length=100)
    nyha = models.CharField(max_length=4)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinical_evaluation'


class KokoroClinicalEvaluationCardiomiopathies(models.Model):
    id = models.BigAutoField(primary_key=True)
    clinical_evaluation = models.ForeignKey(KokoroClinicalEvaluation, models.DO_NOTHING)
    cardiomiopathies = models.ForeignKey(KokoroCardiomiopathies, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinical_evaluation_cardiomiopathies'
        unique_together = (('clinical_evaluation', 'cardiomiopathies'),)


class KokoroClinicalEvaluationComorbidities(models.Model):
    id = models.BigAutoField(primary_key=True)
    clinical_evaluation = models.ForeignKey(KokoroClinicalEvaluation, models.DO_NOTHING)
    comorbidities = models.ForeignKey('KokoroComorbidities', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinical_evaluation_comorbidities'
        unique_together = (('clinical_evaluation', 'comorbidities'),)


class KokoroClinicalEvaluationRiskfactors(models.Model):
    id = models.BigAutoField(primary_key=True)
    clinical_evaluation = models.ForeignKey(KokoroClinicalEvaluation, models.DO_NOTHING)
    riskfactors = models.ForeignKey('KokoroRiskfactors', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinical_evaluation_riskfactors'
        unique_together = (('clinical_evaluation', 'riskfactors'),)


class KokoroClinicalEvaluationSymptoms(models.Model):
    id = models.BigAutoField(primary_key=True)
    clinical_evaluation = models.ForeignKey(KokoroClinicalEvaluation, models.DO_NOTHING)
    symptoms = models.ForeignKey('KokoroSymptoms', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinical_evaluation_symptoms'
        unique_together = (('clinical_evaluation', 'symptoms'),)


class KokoroClinicalevent(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    date = models.DateField()
    clinical_event = models.CharField(max_length=100)
    cause = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_clinicalevent'


class KokoroComorbidities(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_comorbidities'


class KokoroCoronaryintervention(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateField()
    cabg = models.CharField(max_length=1)
    pci = models.CharField(max_length=1)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_coronaryintervention'


class KokoroDeviceevent(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    date = models.DateField()
    n_icd_shock_appropriate_pre_rf = models.IntegerField(blank=True, null=True)
    n_icd_shock_inappropriate_pre_rf = models.IntegerField(blank=True, null=True)
    inappropriate_pre_rf_shock_cause = models.CharField(max_length=4)
    n_icd_shock_appropriate_post_brs_diagnosis = models.IntegerField(blank=True, null=True)
    inappropriate_post_brs_shock_cause = models.CharField(max_length=4)
    complications = models.CharField(max_length=250)
    device = models.ForeignKey('KokoroDeviceinstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_deviceevent'


class KokoroDeviceimplant(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateField()
    lv4_ring = models.FloatField(blank=True, null=True)
    lv3_ring = models.FloatField(blank=True, null=True)
    lv2_ring = models.FloatField(blank=True, null=True)
    lv1_tip = models.FloatField(blank=True, null=True)
    v1 = models.FloatField(blank=True, null=True)
    ms1 = models.IntegerField(blank=True, null=True)
    lv_pulse_configuration_2_lv2 = models.FloatField(blank=True, null=True)
    pacing_impendance1 = models.FloatField(blank=True, null=True)
    v2 = models.FloatField(blank=True, null=True)
    ms2 = models.IntegerField(blank=True, null=True)
    pacing_impendance2 = models.FloatField(blank=True, null=True)
    v3 = models.FloatField(blank=True, null=True)
    ms3 = models.IntegerField(blank=True, null=True)
    pacing_impendance3 = models.FloatField(blank=True, null=True)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_deviceimplant'


class KokoroDeviceinstance(models.Model):
    id = models.UUIDField(primary_key=True)
    serial_number = models.CharField(unique=True, max_length=100)
    implantation = models.OneToOneField(KokoroDeviceimplant, models.DO_NOTHING)
    device_type = models.ForeignKey('KokoroDevicetype', models.DO_NOTHING)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_deviceinstance'


class KokoroDevicetype(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=2)
    company = models.CharField(max_length=2)
    model = models.CharField(max_length=50)
    design = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'kokoro_devicetype'


class KokoroDoctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_doctors'


class KokoroEcg(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_exam = models.DateField()
    max_pressure = models.FloatField(blank=True, null=True)
    min_pressure = models.FloatField(blank=True, null=True)
    atrial_rhythmh = models.CharField(max_length=100)
    hr = models.FloatField(blank=True, null=True)
    rr = models.FloatField(blank=True, null=True)
    pq = models.FloatField(blank=True, null=True)
    pr = models.FloatField(blank=True, null=True)
    qrs = models.FloatField(blank=True, null=True)
    qt = models.FloatField(blank=True, null=True)
    qtc = models.FloatField(blank=True, null=True)
    max_st = models.FloatField(blank=True, null=True)
    rbbb = models.CharField(max_length=3)
    lrbbb = models.CharField(max_length=3)
    irbbb = models.CharField(max_length=3)
    early_rep = models.CharField(max_length=3)
    fragmented_qrs = models.CharField(max_length=3)
    brs = models.CharField(max_length=4)
    av_block = models.CharField(max_length=14)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_ecg'


class KokoroEcho(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_exam = models.DateField()
    max_pressure = models.FloatField(blank=True, null=True)
    min_pressure = models.FloatField(blank=True, null=True)
    lvef = models.FloatField(blank=True, null=True)
    tapse = models.FloatField(blank=True, null=True)
    left_atrial_area = models.FloatField(blank=True, null=True)
    la_diameter = models.FloatField(blank=True, null=True)
    la_end_diastolic_volume = models.FloatField(blank=True, null=True)
    la_end_systolic_volume = models.FloatField(blank=True, null=True)
    lv_end_diastolic_volume = models.FloatField(blank=True, null=True)
    lv_end_systolic_volume = models.FloatField(blank=True, null=True)
    lv_end_diastolic_diameter = models.FloatField(blank=True, null=True)
    lv_end_systolic_diameter = models.FloatField(blank=True, null=True)
    anatomical_alterations = models.CharField(max_length=3)
    aortic_valvulopathy = models.CharField(max_length=3)
    type_of_aortic_valvulopathy = models.CharField(max_length=13)
    severity_of_aortic_valvulopathy = models.CharField(max_length=13)
    mitral_valvulopathy = models.CharField(max_length=3)
    type_of_mitral_valvulopathy = models.CharField(max_length=13)
    severity_of_mitral_valvulopathy = models.CharField(max_length=13)
    tricuspid_valvulopathy = models.CharField(max_length=3)
    type_of_tricuspid_valvulopathy = models.CharField(max_length=13)
    severity_of_tricuspid_valvulopathy = models.CharField(max_length=13)
    diastolic_function = models.CharField(max_length=3)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_echo'


class KokoroEpStudy(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_provocative_test = models.DateField()
    ep_result = models.CharField(max_length=9)
    induced_arrhythmia = models.CharField(max_length=9)
    total_area = models.FloatField(blank=True, null=True)
    bas_area_a_160 = models.FloatField(blank=True, null=True)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_ep_study'


class KokoroFlecainideTest(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_provocative_test = models.DateField()
    flecainide_dose = models.FloatField(blank=True, null=True)
    flecainide_result = models.CharField(max_length=9)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_flecainide_test'


class KokoroGene(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_gene'


class KokoroGeneticProfile(models.Model):
    id = models.UUIDField(primary_key=True)
    fin_progressive_genetics = models.IntegerField(db_column='FIN_progressive_genetics', blank=True, null=True)  # Field name made lowercase.
    fin_number = models.CharField(db_column='FIN_number', max_length=100)  # Field name made lowercase.
    pin_number = models.CharField(db_column='PIN_number', max_length=100)  # Field name made lowercase.
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_profile'


class KokoroGeneticSample(models.Model):
    id = models.UUIDField(primary_key=True)
    blood_sample_date = models.DateField()
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_sample'


class KokoroGeneticStatus(models.Model):
    id = models.UUIDField(primary_key=True)
    patient_status = models.CharField(max_length=100)
    proband_familiarity = models.CharField(max_length=100)
    familiaritytype = models.CharField(db_column='familiarityType', max_length=100)  # Field name made lowercase.
    cardio_fenotypes = models.CharField(max_length=100, blank=True, null=True)
    pato_fenotypes = models.CharField(max_length=100, blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)
    family_degree = models.CharField(max_length=100)
    children = models.IntegerField(blank=True, null=True)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_status'


class KokoroGeneticTest(models.Model):
    id = models.UUIDField(primary_key=True)
    consent_date = models.DateField(db_column='Consent_date')  # Field name made lowercase.
    processingtype = models.CharField(db_column='processingType', max_length=100)  # Field name made lowercase.
    testtype = models.CharField(db_column='testType', max_length=100)  # Field name made lowercase.
    test_category = models.CharField(max_length=100)
    chan_subcategory = models.CharField(max_length=100)
    card_subcategory = models.CharField(max_length=100)
    dys_subcategory = models.CharField(max_length=100)
    coll_subcategory = models.CharField(max_length=100)
    neuro_subcategory = models.CharField(max_length=100)
    metabolic_subcategory = models.CharField(max_length=100)
    onco_subcategory = models.CharField(max_length=100)
    ngstest_result = models.CharField(db_column='NGStest_result', max_length=100)  # Field name made lowercase.
    acmg = models.CharField(db_column='ACMG', max_length=100)  # Field name made lowercase.
    mutunatest_result = models.CharField(db_column='Mutunatest_result', max_length=100)  # Field name made lowercase.
    gene_type = models.CharField(max_length=100)
    zygosity = models.CharField(max_length=100)
    sampletype = models.CharField(db_column='sampleType', max_length=100)  # Field name made lowercase.
    aliquota = models.IntegerField(blank=True, null=True)
    corsa_ngs = models.CharField(db_column='corsa_NGS', max_length=3)  # Field name made lowercase.
    corsa_name = models.CharField(max_length=100)
    sangen = models.CharField(max_length=100)
    sangen_result = models.CharField(db_column='Sangen_result', max_length=100)  # Field name made lowercase.
    reported = models.CharField(max_length=100)
    report_data = models.DateField()
    eredity = models.CharField(max_length=100)
    cromo_anomality = models.CharField(max_length=100)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test'


class KokoroGeneticTestEditingDoctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    genetic_test = models.ForeignKey(KokoroGeneticTest, models.DO_NOTHING)
    doctors = models.ForeignKey(KokoroDoctors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test_editing_doctor'
        unique_together = (('genetic_test', 'doctors'),)


class KokoroGeneticTestGenes(models.Model):
    id = models.BigAutoField(primary_key=True)
    genetic_test = models.ForeignKey(KokoroGeneticTest, models.DO_NOTHING)
    gene = models.ForeignKey(KokoroGene, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test_genes'
        unique_together = (('genetic_test', 'gene'),)


class KokoroGeneticTestReportingDoctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    genetic_test = models.ForeignKey(KokoroGeneticTest, models.DO_NOTHING)
    doctors = models.ForeignKey(KokoroDoctors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test_reporting_doctor'
        unique_together = (('genetic_test', 'doctors'),)


class KokoroGeneticTestVarC(models.Model):
    id = models.BigAutoField(primary_key=True)
    genetic_test = models.ForeignKey(KokoroGeneticTest, models.DO_NOTHING)
    mutation = models.ForeignKey('KokoroMutation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test_var_c'
        unique_together = (('genetic_test', 'mutation'),)


class KokoroGeneticTestVarP(models.Model):
    id = models.BigAutoField(primary_key=True)
    genetic_test = models.ForeignKey(KokoroGeneticTest, models.DO_NOTHING)
    mutation = models.ForeignKey('KokoroMutation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_genetic_test_var_p'
        unique_together = (('genetic_test', 'mutation'),)


class KokoroLatePotentials(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_exam = models.DateField()
    max_pressure = models.FloatField(blank=True, null=True)
    min_pressure = models.FloatField(blank=True, null=True)
    basal_lp1 = models.FloatField(blank=True, null=True)
    basal_lp2 = models.FloatField(blank=True, null=True)
    basal_lp3 = models.FloatField(blank=True, null=True)
    basal_lp4 = models.FloatField(blank=True, null=True)
    patient = models.ForeignKey('KokoroPatientprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_late_potentials'


class KokoroMutation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_mutation'


class KokoroPatientprofile(models.Model):
    id = models.UUIDField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    nation = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    cardioref_id = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_patientprofile'


class KokoroPatientprofileAllergies(models.Model):
    id = models.BigAutoField(primary_key=True)
    patientprofile = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)
    therapy = models.ForeignKey('KokoroTherapy', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_patientprofile_allergies'
        unique_together = (('patientprofile', 'therapy'),)


class KokoroPatientprofileStudies(models.Model):
    id = models.BigAutoField(primary_key=True)
    patientprofile = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)
    study = models.ForeignKey('KokoroStudy', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_patientprofile_studies'
        unique_together = (('patientprofile', 'study'),)


class KokoroPatientprofileTherapies(models.Model):
    id = models.BigAutoField(primary_key=True)
    patientprofile = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)
    therapy = models.ForeignKey('KokoroTherapy', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_patientprofile_therapies'
        unique_together = (('patientprofile', 'therapy'),)


class KokoroPatientstudy(models.Model):
    id = models.BigAutoField(primary_key=True)
    enrollment_date = models.DateField()
    patient = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)
    study = models.ForeignKey('KokoroStudy', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_patientstudy'
        unique_together = (('patient', 'study'),)


class KokoroResearchanalysis(models.Model):
    id = models.UUIDField(primary_key=True)
    analysis_name = models.CharField(max_length=250)
    type = models.CharField(max_length=10)
    date_performed = models.DateField()
    result_files = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kokoro_researchanalysis'


class KokoroResearchanalysisSamples(models.Model):
    id = models.BigAutoField(primary_key=True)
    researchanalysis = models.ForeignKey(KokoroResearchanalysis, models.DO_NOTHING)
    sample = models.ForeignKey('KokoroSample', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_researchanalysis_samples'
        unique_together = (('researchanalysis', 'sample'),)


class KokoroRiskfactors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_riskfactors'


class KokoroRmnTcPh(models.Model):
    id = models.UUIDField(primary_key=True)
    date_of_exam = models.DateField()
    max_pressure = models.FloatField(blank=True, null=True)
    min_pressure = models.FloatField(blank=True, null=True)
    anatomical_alterations = models.CharField(max_length=3)
    lge = models.CharField(max_length=3)
    type_of_lge = models.CharField(max_length=9)
    location_of_lge = models.CharField(max_length=5)
    patient = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_rmn_tc_ph'


class KokoroSample(models.Model):
    id = models.UUIDField(primary_key=True)
    imtc_id = models.CharField(max_length=20)
    procedure_type = models.CharField(max_length=2)
    informed_consent = models.CharField(max_length=20)
    collection_date = models.DateField()
    pbmc_vials_n = models.IntegerField(blank=True, null=True)
    pellet_vials_n = models.IntegerField(blank=True, null=True)
    rna_vials_n = models.IntegerField(blank=True, null=True)
    plasma_cold_vials_n = models.IntegerField(blank=True, null=True)
    plasma_ambient_vials_n = models.IntegerField(blank=True, null=True)
    rin = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=250)
    patient = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_sample'


class KokoroStudy(models.Model):
    id = models.UUIDField(primary_key=True)
    project_code = models.CharField(unique=True, max_length=100)
    project_id = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kokoro_study'


class KokoroSymptoms(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_symptoms'


class KokoroTherapy(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'kokoro_therapy'


class KokoroValveintervention(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateField()
    replacement = models.CharField(max_length=1)
    repair = models.CharField(max_length=1)
    patient = models.ForeignKey(KokoroPatientprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kokoro_valveintervention'


class PatientsAnalysis(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=10)
    date_performed = models.DateField()
    result_files = models.JSONField(blank=True, null=True)
    performed_by = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING, blank=True, null=True)
    analysis_name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'patients_analysis'


class PatientsAnalysisSamples(models.Model):
    id = models.BigAutoField(primary_key=True)
    analysis = models.ForeignKey(PatientsAnalysis, models.DO_NOTHING)
    sample = models.ForeignKey('PatientsSample', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patients_analysis_samples'
        unique_together = (('analysis', 'sample'),)


class PatientsPatient(models.Model):
    id = models.UUIDField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    nation = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    cardioref_id = models.CharField(max_length=100)
    patient_type = models.CharField(max_length=1)
    fin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_patient'


class PatientsSample(models.Model):
    id = models.UUIDField(primary_key=True)
    internal_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    collection_date = models.DateField()
    storage_temperature = models.FloatField()
    freezer_location = models.CharField(max_length=100)
    initial_volume_ml = models.FloatField()
    remaining_volume_ml = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=2)
    quality = models.CharField(max_length=2)
    collected_by = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING, blank=True, null=True)
    patient = models.ForeignKey(PatientsPatient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patients_sample'
