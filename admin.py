from django.contrib import admin

from .models import Payslip

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'period_start', 'period_end', 'gross_salary', 'created_at']
    search_fields = ['employee_name', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

