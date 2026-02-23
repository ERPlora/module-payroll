from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payslips/', views.payslips, name='payslips'),
    path('settings/', views.settings, name='settings'),
]
