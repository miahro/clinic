from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import MyUser, Patients, Diagnoses, Financial, Medicaldata, Intra
import sqlite3
from django.http import Http404
from django.contrib.sessions.models import Session
from . import backend
from datetime import datetime, date
from django.views.decorators.csrf import csrf_protect, csrf_exempt


def index(request):
    return render(request, 'clinic/index.html')

#fix for FLAW 3, add @login required
#@login_required 
def choice(request):
    

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

#fix for FLAW 1: validate that user is autorized to see even patient names        
#    if not backend.role_is_medical(user_id) and not backend.role_is_financial(user):
        #return redirect('index)

    patients = Patients.objects.order_by('id')
    for item in patients:
        item.firstname = backend.decrypt(item.firstname)
        item.lastname = backend.decrypt(item.lastname)
    diagnoses=Diagnoses.objects.order_by('id')
    for item in diagnoses:
        item.description = backend.decrypt(item.description)

    return render(request, 'clinic/choice.html', {"patients": patients, "diagnoses":diagnoses})


#fix for FLAW 3 add login required
# @login_required
def patient(request, patient_id):


    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    #fix for FLAW1: get_patient_data function to be removed
    pdata = backend.get_patient_data(patient_id, user_id)

    #fix for FLAW 1: check role, and choose functionality accordingly
    # if backend.role_is_medical(user):
    #     pdata = backend.get_patient_medical(patient_id, user_id)
    # elif backend.role_is_financial(user):
    #     pdata = backend.get_patient_financial(patient_id, user_id)
    # else:
    #     redirect('index')
    return render(request, 'clinic/patient.html', {"pdata": pdata})


#fix for FLAW 3 add @login required
#login required
#fix for FLAW 7 remove csrf exempt and add csrf token to html-page
@csrf_exempt
def add_diagnosis(request):
    if request.method == "GET":
        return redirect('index')

    patient_id = request.POST['patient']
    diagnose_id = request.POST['diagnose']
    patient = Patients.objects.get(pk=patient_id)
    diagnosis = Diagnoses.objects.get(pk=diagnose_id)
    patient.firstname = backend.decrypt(patient.firstname)
    patient.lastname = backend.decrypt(patient.lastname)
    diagnosis.description = backend.decrypt(diagnosis.description)
    
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d")

    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO clinic_medicaldata (diagnose_id, person_id, diagnose_date) 
            VALUES (%s, %s, '%s') 
        ;'''% (diagnose_id, patient_id, dt))
    conn.commit()
    conn.close()
    return render(request, 'clinic/add_diagnosis.html', {"patient":patient, "diagnosis": diagnosis})

def intra(request): #fix for FLAW 6: remove this view completely
    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        response= cursor.execute('''
            SELECT * FROM clinic_intra 
        ;''')
        conn.commit()
        result = response.fetchall()
        context = {"result": result}
    except:
        print("something wrong in insert")
    conn.close()
    print(result)
    return render(request, 'clinic/intra.html', context)


#this is also POST request without CSRF protection, i.e. FLAW 7
#but as this view will be removed completely as part of fix
#for FLAW 6, CSRF problem doesn't need to be fixed
@csrf_exempt
def add_intra(request): #fix for FLAW 6: remove this view
    if request.method == "GET":
        return redirect('index')

    new_item = request.POST['new_info']
    backend.write_intra(new_item)
    return render(request, 'clinic/add_intra.html', {"added": new_item})
