# Generated by Django 4.1.2 on 2022-11-02 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0022_alter_medicaldata_diagnose_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicaldata",
            name="diagnose_date",
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
