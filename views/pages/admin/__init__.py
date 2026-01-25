"""
Admin Pages - Export all admin pages
"""

from .dashboard import AdminDashboard
from .reports import SystemReportsPage

# Placeholder for pages not yet fully implemented
try:
    from .user_management import UserManagementPage
except:
    UserManagementPage = None

try:
    from .system_config import SystemConfigPage
except:
    SystemConfigPage = None

__all__ = [
    'AdminDashboard',
    'SystemReportsPage',
    'UserManagementPage',
    'SystemConfigPage'
]
