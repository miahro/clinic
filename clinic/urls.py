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
	path('intra/', views.intra, name='intra'), #fix for FLAW 6: remove this view
	path('add_diagnosis/', views.add_diagnosis, name='add_diagnosis'), 
	path('add_intra/', views.add_intra, name='add_intra') #fix for FLAW 6: remove this view

]
