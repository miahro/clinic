from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.



class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_staff = models.BooleanField(default=False)
    #fix for FLAW 1 
    #remove clinic_staff field
    #add financial_staff = models.BooleanField(default=False)
    #add medical_staff = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Patients(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)

    def __str__(self):
        return str(self.pk)


class Financial(models.Model):
    creditcard = models.CharField(max_length=30)
    person = models.ForeignKey(Patients, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)



class Diagnoses(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.pk)


class Medicaldata(models.Model):
    diagnose_date = models.DateField(default=datetime.now)
    diagnose = models.ForeignKey(Diagnoses, on_delete=models.CASCADE)
    person = models.ForeignKey(Patients, on_delete=models.CASCADE)    
    def __str__(self):
        return str(self.pk)

class Intra(models.Model):
    info = models.CharField(max_length=300)
