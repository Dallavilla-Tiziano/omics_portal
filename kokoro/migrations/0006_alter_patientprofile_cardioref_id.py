# Generated by Django 5.1.6 on 2025-05-27 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kokoro', '0005_alter_patientprofile_cardioref_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='cardioref_id',
            field=models.PositiveIntegerField(blank=True, default=''),
        ),
    ]
