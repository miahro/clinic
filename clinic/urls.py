from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .models import MyUser, Patients, Financial, Diagnoses, Medicaldata, Intra
from . import backend
from . import views
from datetime import datetime

#app_name = 'clinic'

urlpatterns = [
	path('', views.index, name='index'),
  	path('login/', LoginView.as_view(template_name='clinic/login.html')),
	path('logout/', LogoutView.as_view(next_page='/clinic')),
	path('choice/', views.choice, name='choice'),
	path('patient/<int:patient_id>', views.patient, name='patient'),
	path('intra/', views.intra, name='intra'),
	path('add_diagnosis/', views.add_diagnosis, name='add_diagnosis'),
	path('add_intra/', views.add_intra, name='add_intra')

]


def startup(): #populate database for testing
	p1, created = Patients.objects.get_or_create(
		firstname=backend.encrypt("Sandy"),
		lastname=backend.encrypt("Sick"))

	p2, created = Patients.objects.get_or_create(
		firstname=backend.encrypt("Pat"),
		lastname=backend.encrypt("Patient"))

	p3, created = Patients.objects.get_or_create(
		firstname=backend.encrypt("Ian"),
		lastname=backend.encrypt("Ill"))

	now = datetime.now()
	dt = now.strftime("%d/%m/%Y")

	d1, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Diarhea"))
	d2, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Drug abuse problem"))
	d3, created = Diagnoses.objects.get_or_create(description=backend.encrypt("COVID-19"))
	d4, created = Diagnoses.objects.get_or_create(description=backend.encrypt("Hemorrhage"))
	f1, created = Financial.objects.get_or_create(creditcard=backend.encrypt("Amex1234"), person=p1)
	f2, created = Financial.objects.get_or_create(creditcard=backend.encrypt("MasterCard1234"), person=p2)
	f3, created = Financial.objects.get_or_create(creditcard=backend.encrypt("Diners1234"), person=p3)
	m1, created = Medicaldata.objects.get_or_create(diagnose_date=now, diagnose=d1, person=p2)
	m2, created = Medicaldata.objects.get_or_create(diagnose_date=now,diagnose=d2, person=p3)
	m3, created = Medicaldata.objects.get_or_create(diagnose_date=now,diagnose=d3, person=p1)
	m4, created = Medicaldata.objects.get_or_create(diagnose_date=now,diagnose=d2, person=p1)
	m5, created = Medicaldata.objects.get_or_create(diagnose_date=now,diagnose=d1, person=p1)

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

startup()
