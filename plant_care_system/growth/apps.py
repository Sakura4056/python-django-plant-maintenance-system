# plant_care_system/growth/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GrowthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'growth'
    verbose_name = _('Growth Tracking')