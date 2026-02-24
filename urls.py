from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Payslip
    path('payslips/', views.payslips_list, name='payslips_list'),
    path('payslips/add/', views.payslip_add, name='payslip_add'),
    path('payslips/<uuid:pk>/edit/', views.payslip_edit, name='payslip_edit'),
    path('payslips/<uuid:pk>/delete/', views.payslip_delete, name='payslip_delete'),
    path('payslips/bulk/', views.payslips_bulk_action, name='payslips_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
