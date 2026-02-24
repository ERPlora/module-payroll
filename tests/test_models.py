"""Tests for payroll models."""
import pytest
from django.utils import timezone

from payroll.models import Payslip


@pytest.mark.django_db
class TestPayslip:
    """Payslip model tests."""

    def test_create(self, payslip):
        """Test Payslip creation."""
        assert payslip.pk is not None
        assert payslip.is_deleted is False

    def test_soft_delete(self, payslip):
        """Test soft delete."""
        pk = payslip.pk
        payslip.is_deleted = True
        payslip.deleted_at = timezone.now()
        payslip.save()
        assert not Payslip.objects.filter(pk=pk).exists()
        assert Payslip.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, payslip):
        """Test default queryset excludes deleted."""
        payslip.is_deleted = True
        payslip.deleted_at = timezone.now()
        payslip.save()
        assert Payslip.objects.filter(hub_id=hub_id).count() == 0


