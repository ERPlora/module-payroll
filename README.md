# Payroll Module

Payroll calculation, deductions and payslip management.

## Features

- Payslip generation with gross salary, deductions, and net salary calculation
- Payslip status workflow: draft, confirmed, paid, cancelled
- Pay period tracking with start and end dates
- Employee reference linking via UUID
- Payment date recording for paid payslips
- Notes field for additional payslip details

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Payroll > Settings**

## Usage

Access via: **Menu > Payroll**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/payroll/dashboard/` | Payroll overview and summary statistics |
| Payslips | `/m/payroll/payslips/` | Create and manage employee payslips |
| Settings | `/m/payroll/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Payslip` | Payslip record with employee reference, pay period dates, gross salary, deductions, net salary, status, paid date, and notes |

## Permissions

| Permission | Description |
|------------|-------------|
| `payroll.view_payslip` | View payslips |
| `payroll.add_payslip` | Create new payslips |
| `payroll.change_payslip` | Edit payslip details |
| `payroll.delete_payslip` | Delete payslips |
| `payroll.manage_settings` | Access and modify module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
