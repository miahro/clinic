
from datetime import datetime
# from django.utils import timezone

def write_log(details):
    # print(details)
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    log = f"{dt}, User_id: {details['user']}, Patient_id: {details['patient_id']}, Query: {details['query']}\n"
    # print(log)
    with open('log.txt', 'a') as f:
        f.write(log)
    print("did we get here?")

def encrypt(plain):
    crypted = ''
    for i in range(len(plain)):
        crypted += chr(ord(plain[i])+1)
    return crypted

def decrypt(crypted):
    plain=''
    for i in range(len(crypted)):
        plain += chr(ord(crypted[i])-1)
    return plain

