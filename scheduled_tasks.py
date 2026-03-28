"""Scheduled task handlers for payroll module."""
import logging
logger = logging.getLogger(__name__)

def generate_monthly_payslips(payload):
    """Generate monthly payslips for all active employees."""
    logger.info('payroll.generate_monthly_payslips called')
    return {'status': 'not_implemented'}
