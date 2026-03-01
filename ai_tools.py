"""AI tools for the Payroll module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListPayslips(AssistantTool):
    name = "list_payslips"
    description = "List payslips with filters."
    module_id = "payroll"
    required_permission = "payroll.view_payslip"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "draft, confirmed, paid, cancelled"},
            "employee_id": {"type": "string"}, "limit": {"type": "integer"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from payroll.models import Payslip
        qs = Payslip.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('employee_id'):
            qs = qs.filter(employee_id=args['employee_id'])
        limit = args.get('limit', 20)
        return {"payslips": [{"id": str(p.id), "employee_name": p.employee_name, "period_start": str(p.period_start), "period_end": str(p.period_end), "gross_salary": str(p.gross_salary), "deductions": str(p.deductions), "net_salary": str(p.net_salary), "status": p.status} for p in qs.order_by('-period_start')[:limit]]}


@register_tool
class CreatePayslip(AssistantTool):
    name = "create_payslip"
    description = "Create a payslip."
    module_id = "payroll"
    required_permission = "payroll.add_payslip"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string"}, "employee_name": {"type": "string"},
            "period_start": {"type": "string"}, "period_end": {"type": "string"},
            "gross_salary": {"type": "string"}, "deductions": {"type": "string"},
            "notes": {"type": "string"},
        },
        "required": ["employee_id", "employee_name", "period_start", "period_end", "gross_salary"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from payroll.models import Payslip
        gross = Decimal(args['gross_salary'])
        deductions = Decimal(args.get('deductions', '0'))
        p = Payslip.objects.create(
            employee_id=args['employee_id'], employee_name=args['employee_name'],
            period_start=args['period_start'], period_end=args['period_end'],
            gross_salary=gross, deductions=deductions, net_salary=gross - deductions,
            notes=args.get('notes', ''),
        )
        return {"id": str(p.id), "net_salary": str(p.net_salary), "created": True}


@register_tool
class UpdatePayslipStatus(AssistantTool):
    name = "update_payslip_status"
    description = "Update payslip status: confirm (draft→confirmed), pay (confirmed→paid), cancel."
    module_id = "payroll"
    required_permission = "payroll.change_payslip"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "payslip_id": {"type": "string", "description": "Payslip ID"},
            "action": {"type": "string", "description": "Action: confirm, pay, cancel"},
        },
        "required": ["payslip_id", "action"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from django.utils import timezone
        from payroll.models import Payslip
        p = Payslip.objects.get(id=args['payslip_id'])
        action = args['action']
        if action == 'confirm' and p.status == 'draft':
            p.status = 'confirmed'
        elif action == 'pay' and p.status == 'confirmed':
            p.status = 'paid'
            p.paid_date = timezone.now().date()
        elif action == 'cancel' and p.status in ('draft', 'confirmed'):
            p.status = 'cancelled'
        else:
            return {"error": f"Cannot {action} a {p.status} payslip"}
        p.save(update_fields=['status', 'paid_date'] if action == 'pay' else ['status'])
        return {"id": str(p.id), "employee_name": p.employee_name, "status": p.status}


@register_tool
class GetPayrollSummary(AssistantTool):
    name = "get_payroll_summary"
    description = "Get payroll summary for a period: total gross, deductions, net, count by status."
    module_id = "payroll"
    required_permission = "payroll.view_payslip"
    parameters = {
        "type": "object",
        "properties": {
            "period_start": {"type": "string", "description": "Period start date (YYYY-MM-DD)"},
            "period_end": {"type": "string", "description": "Period end date (YYYY-MM-DD)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from django.db.models import Sum, Count
        from payroll.models import Payslip
        qs = Payslip.objects.all()
        if args.get('period_start'):
            qs = qs.filter(period_start__gte=args['period_start'])
        if args.get('period_end'):
            qs = qs.filter(period_end__lte=args['period_end'])
        totals = qs.aggregate(
            total_gross=Sum('gross_salary'),
            total_deductions=Sum('deductions'),
            total_net=Sum('net_salary'),
            count=Count('id'),
        )
        by_status = {}
        for status in ('draft', 'confirmed', 'paid', 'cancelled'):
            by_status[status] = qs.filter(status=status).count()
        return {
            "total_gross": str(totals['total_gross'] or 0),
            "total_deductions": str(totals['total_deductions'] or 0),
            "total_net": str(totals['total_net'] or 0),
            "count": totals['count'],
            "by_status": by_status,
        }
