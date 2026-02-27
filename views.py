"""
Payroll Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Payslip

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('payroll', 'dashboard')
@htmx_view('payroll/pages/index.html', 'payroll/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_payslips': Payslip.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Payslip
# ======================================================================

PAYSLIP_SORT_FIELDS = {
    'status': 'status',
    'net_salary': 'net_salary',
    'deductions': 'deductions',
    'gross_salary': 'gross_salary',
    'employee_id': 'employee_id',
    'employee_name': 'employee_name',
    'created_at': 'created_at',
}

def _build_payslips_context(hub_id, per_page=10):
    qs = Payslip.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'payslips': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_payslips_list(request, hub_id, per_page=10):
    ctx = _build_payslips_context(hub_id, per_page)
    return django_render(request, 'payroll/partials/payslips_list.html', ctx)

@login_required
@with_module_nav('payroll', 'payslips')
@htmx_view('payroll/pages/payslips.html', 'payroll/partials/payslips_content.html')
def payslips_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Payslip.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(employee_name__icontains=search_query) | Q(status__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = PAYSLIP_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'net_salary', 'deductions', 'gross_salary', 'employee_id', 'employee_name']
        headers = ['Status', 'Net Salary', 'Deductions', 'Gross Salary', 'Employee Id', 'Employee Name']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='payslips.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='payslips.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'payroll/partials/payslips_list.html', {
            'payslips': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'payslips': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def payslip_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        employee_name = request.POST.get('employee_name', '').strip()
        period_start = request.POST.get('period_start') or None
        period_end = request.POST.get('period_end') or None
        gross_salary = request.POST.get('gross_salary', '0') or '0'
        deductions = request.POST.get('deductions', '0') or '0'
        net_salary = request.POST.get('net_salary', '0') or '0'
        status = request.POST.get('status', '').strip()
        paid_date = request.POST.get('paid_date') or None
        notes = request.POST.get('notes', '').strip()
        obj = Payslip(hub_id=hub_id)
        obj.employee_id = employee_id
        obj.employee_name = employee_name
        obj.period_start = period_start
        obj.period_end = period_end
        obj.gross_salary = gross_salary
        obj.deductions = deductions
        obj.net_salary = net_salary
        obj.status = status
        obj.paid_date = paid_date
        obj.notes = notes
        obj.save()
        return _render_payslips_list(request, hub_id)
    return django_render(request, 'payroll/partials/panel_payslip_add.html', {})

@login_required
def payslip_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Payslip, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.employee_id = request.POST.get('employee_id', '').strip()
        obj.employee_name = request.POST.get('employee_name', '').strip()
        obj.period_start = request.POST.get('period_start') or None
        obj.period_end = request.POST.get('period_end') or None
        obj.gross_salary = request.POST.get('gross_salary', '0') or '0'
        obj.deductions = request.POST.get('deductions', '0') or '0'
        obj.net_salary = request.POST.get('net_salary', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.paid_date = request.POST.get('paid_date') or None
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_payslips_list(request, hub_id)
    return django_render(request, 'payroll/partials/panel_payslip_edit.html', {'obj': obj})

@login_required
@require_POST
def payslip_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Payslip, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_payslips_list(request, hub_id)

@login_required
@require_POST
def payslips_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Payslip.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_payslips_list(request, hub_id)


@login_required
@permission_required('payroll.manage_settings')
@with_module_nav('payroll', 'settings')
@htmx_view('payroll/pages/settings.html', 'payroll/partials/settings_content.html')
def settings_view(request):
    return {}

