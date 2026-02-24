from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Payslip

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ['employee_id', 'employee_name', 'period_start', 'period_end', 'gross_salary', 'deductions', 'net_salary', 'status', 'paid_date', 'notes']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'employee_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'period_start': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'period_end': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'gross_salary': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'deductions': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'net_salary': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'paid_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

