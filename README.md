# Clinic Patient Management System

## Purpose
This Django app is project work I for Helsinki University course Cyber Security Base 2022.

## Important notes
The purpose of the project is to demonstrate application security risks. I.e. securerity features of the application are purposefully done wrong. This app should not be used for anything execpt testing related to Cyber Security Base course, as it is totally unsecure. 

## Features
App is customer database for medical clinic. It contains:
- Users:
    - Staff of clinic (medical, admin and support staff)
    - Patients
- Data for patients, including:
    - personal details
    - financial details (credit card number)
    - diagnoses 
- Company intranet: 
    - general announcements


Main functionalities:
- Staff can:
    - check patiend data
    - add diagnoses (from preset diagnosis list)
    - view intranet announcements
    - add new announcemements to intranet

## Modules
- clinic/templates: all html-templates used
- _ _ init _ _.py: defines where application configuration is found
- apps.py: configuration functionality, needed to populate sample database
- admin.py: registers database models for Django admin page
- urls.py: url's for views app is using
- backend.py: business logics functionality is placed here to keep views module reasonably short
- views.py: functionality for various views
- database used by app has default name "db.sqlite3"
    - note! this has been hardcoded in the app, doesn't work if db name is changed

## Installation instructions
The app is using Django platform, and is meant to run in development mode only. To install:
- clone repository to your local machine
- make database migrations:
    - python3 manage.py migrate
    - python3 manage.py makemigrations
- start server
    - python3 manage.py runserver
- access server at 127.0.0.1:8000/clinic/


## Test dataset
At server startup small database for testing/demonstration purposes is created. It contains following data:
- Sample users (medical, financial admin and support staff)
    - Danielle Doctor, username "doc", password 12345
    - Adam Administrator, username "admin", password 12345
    - Mike Maintenance, username "maint", password 12345
- Sample Patients:
    - Sandy Sick
    - Pat Patient
    - Ian Ill
- Financial:
    - credit card number
    - refernced to patient id
- Diagnoses:
    - Diarrhea
    - Drug abuse problem
    - COVID-19
    - Hemorrhage
- Medical data:
    - diagnose date
    - diagnose_id referencing to diagnoses table
    - patient_id referencing to patients
- Intra
    - information /  announcmements for company intranet

## Notes
As the purpose is only to demonstrate security vulnerabilities, the functionality is rather limited. There is for example no functionality to:
- create new users
- add new diagnoses (only preset short list included)
- add new financial data (only fixed set credit card no per patient)

all these could be easily added, but as this would provide no added value for demonstrating security risks, it is not done. 

