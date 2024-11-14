from django.apps import AppConfig


class AdminappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminapp'
# apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'adminapp'

    def ready(self):
        import adminapp.signals
