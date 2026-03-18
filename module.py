from django.utils.translation import gettext_lazy as _

MODULE_ID = 'payroll'
MODULE_NAME = _('Payroll')
MODULE_VERSION = '1.0.1'
MODULE_ICON = 'material:account_balance_wallet'
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

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_payslip",
        "change_payslip",
        "view_payslip",
    ],
    "employee": [
        "add_payslip",
        "view_payslip",
    ],
}
