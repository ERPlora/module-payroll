"""
AI context for the Payroll module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Payroll

### Models

**Payslip**
- employee_id (UUID, indexed) — references StaffMember or LocalUser UUID
- employee_name (str, cached for display)
- period_start, period_end (DateField) — the pay period
- gross_salary (Decimal), deductions (Decimal), net_salary (Decimal)
- status: draft | confirmed | paid | cancelled
- paid_date (DateField, optional) — set when status becomes paid
- notes (text)

### Key flows

1. **Create payslip**: Set employee_id + employee_name, period_start/end, gross_salary, deductions; net_salary = gross_salary - deductions; status defaults to draft
2. **Confirm payslip**: Change status from draft → confirmed after reviewing figures
3. **Mark as paid**: Change status to paid, set paid_date
4. **Cancel payslip**: Change status to cancelled (no deletion)

### Notes

- employee_id is a UUID that should match the staff member's primary key
- net_salary must be calculated before saving (not auto-computed by the model)
- There is no direct FK to StaffMember — the link is via employee_id UUID
- Multiple payslips can exist for the same employee across different periods
"""
