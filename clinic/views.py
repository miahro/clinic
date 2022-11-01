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

# Create your views here.


def index(request):

    # p="testisana"
    # print(p)
    # c=backend.encrypt(p)
    # print(c)
    # e=backend.decrypt(c)
    # print(e)
   

    return render(request, 'clinic/index.html')


# @login_required
def choice(request):
    patients = Patients.objects.order_by('id')
    # print(type(patients))
    for item in patients:
        # print(item.id)
        item.firstname = backend.decrypt(item.firstname)
        item.lastname = backend.decrypt(item.lastname)
        # print(item.lastname)
    diagnoses=Diagnoses.objects.order_by('id')
    for item in diagnoses:
        item.description = backend.decrypt(item.description)

    return render(request, 'clinic/choice.html', {"patients": patients, "diagnoses":diagnoses})
#    return HttpResponse(template.render(context, request))

# @csrf_protect
# @login_required
def patient(request, patient_id):
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        is_staff = MyUser.objects.get(user=user).clinic_staff
        # print(is_staff)
        # print(type(is_staff))

    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    response = cursor.execute('''
        SELECT firstname, lastname, creditcard, description
        FROM clinic_patients, clinic_financial, clinic_diagnoses, clinic_medicaldata
        WHERE clinic_medicaldata.diagnose_id = clinic_diagnoses.id
        AND clinic_financial.person_id = clinic_patients.id
        AND clinic_medicaldata.person_id = clinic_patients.id
        AND clinic_patients.id='%s'
    ;'''% (patient_id))
    # try:
    result = response.fetchall()
    # except:
    #     print("joku kämähtää tässä")
    conn.commit()
    conn.close()
    # print(f"result {result}")
    # for row in result:
    #     # print(f"item[0] {item[0]}")
    #     # print(len(item))
    #     for i in range(1,5):
    #          row[i]=backend.decrypt(row[i])

    # print(result)
    pdata = [[backend.decrypt(item) for item in row] for row in result]
    # print(pdata)

    keys=["firstname", "lastname", "creditcard", "diagnosis"]
    # print(f"pdata after decrypt {pdata}")


    log_details = {"user": user_id, "patient_id": patient_id, "query": "all data"}
    backend.write_log(log_details)

    return render(request, 'clinic/patient.html', {"pdata": pdata})

def intra(request):
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

@csrf_exempt
def add_diagnosis(request):
    if request.method == "GET":
        return redirect('index')

    patient_id = request.POST['patient']
    diagnose_id = request.POST['diagnose']

    # print(f"in vies.add_diagnosis form return patient_id {patient_id} diagnose_id {diagnose_id}")

    
    patient = Patients.objects.get(pk=patient_id)
    diagnosis = Diagnoses.objects.get(pk=diagnose_id)
    patient.firstname = backend.decrypt(patient.firstname)
    patient.lastname = backend.decrypt(patient.lastname)
    diagnosis.description = backend.decrypt(diagnosis.description)
    # print(patient.id)
    # print(patient.firstname)
    # print(patient.lastname)
    # print(diagnosis)

    now = datetime.now()
    # print(now)
    dt = now.strftime("%Y-%m-%d")
    # print(dt)

    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clinic_medicaldata (diagnose_id, person_id, diagnose_date) 
            VALUES (%s, %s, '%s') 
        ;'''% (diagnose_id, patient_id, dt))
        conn.commit()
        print(f"cursor.rowcount {cursor.rowcount}")
    except:
        print("something wrong in insert")
    conn.close()
      
    return render(request, 'clinic/add_diagnosis.html', {"patient":patient, "diagnosis": diagnosis})

@csrf_exempt
def add_intra(request):
    if request.method == "GET":
        return redirect('index')

    new_item = request.POST['new_info']

    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    try:
        cursor.executescript('''
            INSERT INTO clinic_intra (info) 
            VALUES ('%s') 
        ;'''% (new_item))
        conn.commit()
        print(f"cursor.rowcount {cursor.rowcount}")
    except:
        print("something wrong in insert")
    conn.close()
    return render(request, 'clinic/add_intra.html', {"added": new_item})



# def write_log(details):
    # print(details)
    # now = datetime.now()
    # dt = now.strftime("%d/%m/%Y %H:%M:%S")
    # log = f"{dt}, User_id: {details['user']}, Patient_id: {details['patient_id']}, Query: {details['query']}\n"
    # print(log)
    # with open('log.txt', 'a') as f:
    #     f.write(log)
    # print("did we get here?")