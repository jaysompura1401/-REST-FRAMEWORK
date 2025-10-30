from django.contrib import admin
from .models import Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','specialty','city','address','latitude','longitude','created_at')
