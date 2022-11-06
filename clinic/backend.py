
from datetime import datetime
import sqlite3


#fix for FLAW5 add log-file function for database access
def write_log(details):
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    log = f"{dt}, User_id: {details['user']}, Patient_id: {details['patient_id']}, Query: {details['query']}\n"
    with open('log.txt', 'a') as f:
        f.write(log)



def encrypt(plain):
    crypted = ''
    for i in range(len(plain)):
        crypted += chr(ord(plain[i])+1)
    return crypted
    #fix for FLAW 4: use for example Fernet module
    #from cryptography.fernet import Fernet
    #generate key and store it to non-shared .env etc file
    # KEY = Fernet.generate_key()
    # and redefine this encrypt function:
    # f = Fernet(KEY)
    # return f.encrypt(plain)

def decrypt(crypted):
    plain=''
    for i in range(len(crypted)):
        plain += chr(ord(crypted[i])-1)
    return plain
    #fix for FLAW 4: user Fernet module as above
    #redefine decrypt function as:
    #f = Fernet(KEY)
    #return f.decrypt(crypted)


#fixes for FLAWS 2 and 5 explained below
#fix fore main FLAW 1 is to remove this function completely
#and replace with "get_patient_medical" and "get_patient_financial"
def get_patient_data(patient_id, user_id):
    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    sql = '''
        SELECT diagnose_date, firstname, lastname, creditcard, description
        FROM clinic_patients, clinic_financial, clinic_diagnoses, clinic_medicaldata
        WHERE clinic_medicaldata.diagnose_id = clinic_diagnoses.id
        AND clinic_financial.person_id = clinic_patients.id
        AND clinic_medicaldata.person_id = clinic_patients.id
        AND clinic_patients.id='%s'
    ;'''
    response = cursor.execute(sql % (patient_id))
    #fix SQL injection problem (FLAW 2):
    #replace last row of SQL enquiry with:
    #AND clinic_patients.id=:patient_id
    #and actual enquiry as 
    #response = cursor.execute(sql, {"patient_id":patient_id})

    result = response.fetchall()
    conn.commit()
    conn.close()
    pdata = []
    for item in result:
        temp = []
        temp.append(item[0])
        for i in range(1,5):
            temp.append(decrypt(item[i]))
        pdata.append(temp)
# fix for FLAW 5: write log after each DB operation accessing or changing data
#    log_details = {"user": user_id, "patient_id": patient_id, "query": "all data"}
#    write_log(log_details)
    return pdata


#fix for FLAW 1: separate query for medical data
#fix for FLAW 2: SQL requry paramatrized
#fix for FLAW 5: logging added 
# def get_patient_medical(patient_id, user_id):
#     dbname='db.sqlite3'
#     conn = sqlite3.connect(dbname)
#     cursor = conn.cursor()
#     sql = '''
#         SELECT diagnose_date, firstname, lastname, description
#         FROM clinic_patients, clinic_diagnoses, clinic_medicaldata
#         WHERE clinic_medicaldata.diagnose_id = clinic_diagnoses.id
#         AND clinic_medicaldata.person_id = clinic_patients.id
#         AND clinic_patients.id=:patient_id
#     ;'''

#     #SQL enquiry properly parametrized
#     response = cursor.execute(sql, {"patient_id":patient_id})

#     result = response.fetchall()
#     conn.commit()
#     conn.close()
#     pdata = []
#     for item in result:
#         temp = []
#         temp.append(item[0])
#         for i in range(1,4):
#             temp.append(decrypt(item[i]))
#         pdata.append(temp)
# # fix for FLAW 5: write log after each DB operation accessing or changing data
# #    log_details = {"user": user_id, "patient_id": patient_id, "query": "medical data"}
# #    write_log(log_details)
#     return pdata

#fix for FLAW 1: separate query for financial data
#fix for FLAW 2: parametrized SQL query
#fix for FLAW 5: logging added
# def get_patient_financial(patient_id, user_id):
#     dbname='db.sqlite3'
#     conn = sqlite3.connect(dbname)
#     cursor = conn.cursor()
#     sql = '''
#         SELECT firstname, lastname, creditcard
#         FROM clinic_patients, clinic_financial
#         WHERE clinic_financial.person_id = clinic_patients.id
#         AND clinic_patients.id=:patient_id
#     ;'''
#     #SQL enquiry propeperly parametrized
#     response = cursor.execute(sql, {"patient_id":patient_id})
#     result = response.fetchall()
#     conn.commit()
#     conn.close()
#     pdata = []
#     for item in result:
#         temp = []
#         for i in range(0,3):
#             temp.append(decrypt(item[i]))
#         pdata.append(temp)
# # fix for FLAW 5: write log after each DB operation accessing or changing data
# #    log_details = {"user": user_id, "patient_id": patient_id, "query": "financial data"}
# #    write_log(log_details)
#     return pdata


#fix for FLAW 2: parametrize raw SQL-query
#and replace very dangerous "executescript" with "execute"
#this just for demonstrative purposes, as whole function 
#is removed as per fix for FLAW 6
def write_intra(new_item):
    dbname='db.sqlite3'
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.executescript('''
            INSERT INTO clinic_intra (info) 
            VALUES ('%s') 
        ;'''% (new_item))
    conn.commit()
    conn.close()
#improved version:
        # sql = '''
        #     INSERT INTO clinic_intra (info) 
        #     VALUES ("new_item"=:"new_item) 
        # ;'''
        # cursor.execute(sql, {"new_item": new_item})


#Fix for FLAW 1: proper check of role
#requires that MyUser object has been fixed first, see models.py
# def role_is_medical(user):
#     return MyUser.objecs(user=user).medical_staff

#Fix for FLAW 1: proper check of role
#requires that MyUser object has been fixed first, see models.py
# def role_is_financial(user):
#     return MyUser.objecs(user=user).finacial_staff
