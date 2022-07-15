from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class CyberstickAdminConfig(AdminConfig):
    default_site = 'core.admin.CyberstickAdminSite'

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
