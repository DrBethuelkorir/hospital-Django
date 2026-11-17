from django.contrib import admin

from .models import Patient, Payment


admin.site.register(Patient)
admin.site.register(Payment)