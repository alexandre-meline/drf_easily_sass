from django.apps import AppConfig
from django.conf import settings
from drf_easily_saas.schemas.config import validate_settings

# -------------------------------------------- #
    
class DrfEasilyAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drf_easily_saas"

    def ready(self):
        validate_settings(settings.EASILY)
