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
