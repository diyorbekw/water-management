from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _("Asosiy modullar")
    
    def ready(self):
        # Remove or comment out the signals import
        # import core.signals
        pass