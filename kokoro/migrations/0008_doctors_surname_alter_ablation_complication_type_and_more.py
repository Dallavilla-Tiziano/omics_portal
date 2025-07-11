# Generated by Django 5.1.6 on 2025-06-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kokoro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='surname',
            field=models.CharField(default='rossi', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ablation',
            name='complication_type',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='ablation',
            name='therapy',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='company',
            field=models.CharField(choices=[('', 'Choose a company'), ('AB', 'Abbott'), ('BT', 'Biotronik'), ('MT', 'Medtronic'), ('BS', 'Boston'), ('SJ', 'St. Jude')], max_length=50),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='design',
            field=models.CharField(choices=[('', 'Choose a design'), ('Single\\Dual Pacemaker', 'Sd Pacemaker'), ('Single\\Dual Chamber ICD', 'Sd Chamber Icd'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='model',
            field=models.CharField(choices=[('', 'Choose a model'), ('INTICA 7 HF-TQPDF4/IS4', 'In7F4Is4'), ('RIVACOR 7 HF-T QP', 'Ri7Hfqp'), ('INTICA 7 HF-TQPDF1/IS4', 'In7Hfis4'), ('INTICA NEO 7 HF-T QP', 'Inn7Hfqp')], max_length=50),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='type',
            field=models.CharField(choices=[('', 'Choose a type'), ('CD', 'Cardiac Device'), ('LR', 'Loop Recorder'), ('PM', 'Pace Maker')], max_length=5),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
