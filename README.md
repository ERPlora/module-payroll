# Payroll

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `payroll` |
| **Version** | `1.0.0` |
| **Icon** | `cash-outline` |
| **Dependencies** | None |

## Models

### `Payslip`

Payslip(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, employee_id, employee_name, period_start, period_end, gross_salary, deductions, net_salary, status, paid_date, notes)

| Field | Type | Details |
|-------|------|---------|
| `employee_id` | UUIDField | max_length=32 |
| `employee_name` | CharField | max_length=255 |
| `period_start` | DateField |  |
| `period_end` | DateField |  |
| `gross_salary` | DecimalField |  |
| `deductions` | DecimalField |  |
| `net_salary` | DecimalField |  |
| `status` | CharField | max_length=20, choices: draft, confirmed, paid, cancelled |
| `paid_date` | DateField | optional |
| `notes` | TextField | optional |

## URL Endpoints

Base path: `/m/payroll/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `payslips/` | `payslips_list` | GET |
| `payslips/add/` | `payslip_add` | GET/POST |
| `payslips/<uuid:pk>/edit/` | `payslip_edit` | GET |
| `payslips/<uuid:pk>/delete/` | `payslip_delete` | GET/POST |
| `payslips/bulk/` | `payslips_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `payroll.view_payslip` | View Payslip |
| `payroll.add_payslip` | Add Payslip |
| `payroll.change_payslip` | Change Payslip |
| `payroll.delete_payslip` | Delete Payslip |
| `payroll.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_payslip`, `change_payslip`, `view_payslip`
- **employee**: `add_payslip`, `view_payslip`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Payslips | `cash-outline` | `payslips` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_payslips`

List payslips with filters.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | draft, confirmed, paid, cancelled |
| `employee_id` | string | No |  |
| `limit` | integer | No |  |

### `create_payslip`

Create a payslip.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `employee_id` | string | Yes |  |
| `employee_name` | string | Yes |  |
| `period_start` | string | Yes |  |
| `period_end` | string | Yes |  |
| `gross_salary` | string | Yes |  |
| `deductions` | string | No |  |
| `notes` | string | No |  |

### `update_payslip_status`

Update payslip status: confirm (draft→confirmed), pay (confirmed→paid), cancel.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `payslip_id` | string | Yes | Payslip ID |
| `action` | string | Yes | Action: confirm, pay, cancel |

### `get_payroll_summary`

Get payroll summary for a period: total gross, deductions, net, count by status.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period_start` | string | No | Period start date (YYYY-MM-DD) |
| `period_end` | string | No | Period end date (YYYY-MM-DD) |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  payroll/
    css/
    js/
templates/
  payroll/
    pages/
      dashboard.html
      index.html
      payslip_add.html
      payslip_edit.html
      payslips.html
      settings.html
    partials/
      dashboard_content.html
      panel_payslip_add.html
      panel_payslip_edit.html
      payslip_add_content.html
      payslip_edit_content.html
      payslips_content.html
      payslips_list.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
