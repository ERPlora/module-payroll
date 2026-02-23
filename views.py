"""
Payroll Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('payroll', 'dashboard')
@htmx_view('payroll/pages/dashboard.html', 'payroll/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('payroll', 'payslips')
@htmx_view('payroll/pages/payslips.html', 'payroll/partials/payslips_content.html')
def payslips(request):
    """Payslips view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('payroll', 'settings')
@htmx_view('payroll/pages/settings.html', 'payroll/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

