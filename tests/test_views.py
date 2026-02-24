"""Tests for payroll views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('payroll:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('payroll:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('payroll:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPayslipViews:
    """Payslip view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('payroll:payslips_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('payroll:payslip_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('payroll:payslip_add')
        data = {
            'employee_id': 'test',
            'employee_name': 'New Employee Name',
            'period_start': '2025-01-15',
            'period_end': '2025-01-15',
            'gross_salary': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, payslip):
        """Test edit form loads."""
        url = reverse('payroll:payslip_edit', args=[payslip.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, payslip):
        """Test editing via POST."""
        url = reverse('payroll:payslip_edit', args=[payslip.pk])
        data = {
            'employee_id': 'test',
            'employee_name': 'Updated Employee Name',
            'period_start': '2025-01-15',
            'period_end': '2025-01-15',
            'gross_salary': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, payslip):
        """Test soft delete via POST."""
        url = reverse('payroll:payslip_delete', args=[payslip.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        payslip.refresh_from_db()
        assert payslip.is_deleted is True

    def test_bulk_delete(self, auth_client, payslip):
        """Test bulk delete."""
        url = reverse('payroll:payslips_bulk_action')
        response = auth_client.post(url, {'ids': str(payslip.pk), 'action': 'delete'})
        assert response.status_code == 200
        payslip.refresh_from_db()
        assert payslip.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('payroll:payslips_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('payroll:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('payroll:settings')
        response = client.get(url)
        assert response.status_code == 302

