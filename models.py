from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

PAYSLIP_STATUS = [
    ('draft', _('Draft')),
    ('confirmed', _('Confirmed')),
    ('paid', _('Paid')),
    ('cancelled', _('Cancelled')),
]

class Payslip(HubBaseModel):
    employee_id = models.UUIDField(db_index=True, verbose_name=_('Employee Id'))
    employee_name = models.CharField(max_length=255, verbose_name=_('Employee Name'))
    period_start = models.DateField(verbose_name=_('Period Start'))
    period_end = models.DateField(verbose_name=_('Period End'))
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Gross Salary'))
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Deductions'))
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Net Salary'))
    status = models.CharField(max_length=20, default='draft', choices=PAYSLIP_STATUS, verbose_name=_('Status'))
    paid_date = models.DateField(null=True, blank=True, verbose_name=_('Paid Date'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'payroll_payslip'

    def __str__(self):
        return str(self.id)

