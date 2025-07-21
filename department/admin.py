from django.contrib import admin
from .models import EmployeeProfile

# Register your models here.
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'progress')
