from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import MyUser, Financial, Diagnoses, Patients, Medicaldata, Intra

admin.site.register(MyUser)
admin.site.register(Financial)
admin.site.register(Diagnoses)
admin.site.register(Patients)
admin.site.register(Medicaldata)
admin.site.register(Intra)