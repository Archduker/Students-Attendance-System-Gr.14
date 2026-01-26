"""
Admin Pages - Export all admin pages
"""

from .dashboard import AdminDashboard
from .reports import SystemReportsPage
from .user_management import UserManagementPage
from .class_management import ClassManagementPage

__all__ = [
    'AdminDashboard',
    'SystemReportsPage',
    'UserManagementPage',
    'ClassManagementPage'
]
