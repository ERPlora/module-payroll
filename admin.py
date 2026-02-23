from django.contrib import admin

from .models import Payslip

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'period_start', 'period_end', 'gross_salary']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

