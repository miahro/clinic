# Generated by Django 4.1.2 on 2022-10-21 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Diagnoses",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Persons",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("firstname", models.CharField(max_length=20)),
                ("lastname", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("role", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
                ("role_id", models.IntegerField()),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="clinic.persons"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Patients",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "diagnose_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinic.diagnoses",
                    ),
                ),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="clinic.persons"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Financial",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("creditcard_no", models.CharField(max_length=30)),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="clinic.persons"
                    ),
                ),
            ],
        ),
    ]
