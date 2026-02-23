from django.utils.translation import gettext_lazy as _

MODULE_ID = 'payroll'
MODULE_NAME = _('Payroll')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'cash-outline'
MODULE_DESCRIPTION = _('Payroll calculation, deductions and payslips')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'hr'

MENU = {
    'label': _('Payroll'),
    'icon': 'cash-outline',
    'order': 42,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Payslips'), 'icon': 'cash-outline', 'id': 'payslips'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'payroll.view_payslip',
'payroll.add_payslip',
'payroll.change_payslip',
'payroll.delete_payslip',
'payroll.manage_settings',
]
