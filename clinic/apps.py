
from django.apps import AppConfig
from . import backend


#demo database initiliatization code
#needs to be here so that it is not run during migrations
#but only at start server
def start():
    from .models import Patients, Diagnoses, Financial, Medicaldata, Intra, MyUser
    from datetime import datetime
    from django.contrib.auth.models import User
    p1, created = Patients.objects.get_or_create(
        firstname=backend.encrypt("Sandy"),
        lastname=backend.encrypt("Sick"))

    p2, created = Patients.objects.get_or_create(
        firstname=backend.encrypt("Pat"),
        lastname=backend.encrypt("Patient"))

    p3, created = Patients.objects.get_or_create(
        firstname=backend.encrypt("Ian"),
        lastname=backend.encrypt("Ill"))

    init_date = datetime(2022, 10, 31)
    #dt = now.strftime("%d/%m/%Y")

    d1, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Diarrhea"))
    d2, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Drug abuse problem"))
    d3, created = Diagnoses.objects.get_or_create(description=backend.encrypt("COVID-19"))
    d4, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Hemorrhage"))
    f1, created = Financial.objects.get_or_create(creditcard=backend.encrypt("Amex1234"), person=p1)
    f2, created = Financial.objects.get_or_create(creditcard=backend.encrypt("MasterCard1234"), person=p2)
    f3, created = Financial.objects.get_or_create(creditcard=backend.encrypt("Diners1234"), person=p3)
    m1, created = Medicaldata.objects.get_or_create(diagnose_date=init_date, diagnose=d1, person=p2)
    m2, created = Medicaldata.objects.get_or_create(diagnose_date=init_date,diagnose=d2, person=p3)
    m3, created = Medicaldata.objects.get_or_create(diagnose_date=init_date,diagnose=d3, person=p1)
    m4, created = Medicaldata.objects.get_or_create(diagnose_date=init_date,diagnose=d2, person=p1)
    m5, created = Medicaldata.objects.get_or_create(diagnose_date=init_date,diagnose=d1, person=p1)

    user = User.objects.filter(username="adm")
    if not user.exists():
        newuser=User.objects.create_user(username="adm", first_name="Adam", last_name="Administrator", password="12345")
        myuser = MyUser.objects.create(user=newuser, clinic_staff=True)
        myuser.save()   
    user2 = User.objects.filter(username="doc")
    if not user2.exists():
            newuser2 = User.objects.create_user(username="doc", first_name="Danielle", last_name="Doctor", password="12345")
            myuser2 = MyUser.objects.create(user=newuser2, clinic_staff=True)
            myuser2.save()
    user3 = User.objects.filter(username="maint")
    if not user3.exists():
            newuser3 = User.objects.create_user(username="maint", first_name="Mike", last_name="Maintence", password="12345")
            myuser3 = MyUser.objects.create(user=newuser3, clinic_staff=True)
            myuser3.save()

    company_info = [
        "Casual Friday with snacks",
        "Our company is great place to work",
        "Parking spots marked 'Doctor' are for DOCTORS ONLY!",
        "Clean your shoes before entering clinic ",
        "Wash your hands",
        "You are all reminded about importance of IT security"
    ]

    for item in company_info:
        info_item = Intra.objects.filter(info=item)
        if not info_item.exists():
            new_info = Intra.objects.create(info=item)
            new_info.save()


class ClinicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clinic"
    verbose_name ="Clinic"
    def ready(self):
        import os 
        if os.environ.get('RUN_MAIN'):
            start()
