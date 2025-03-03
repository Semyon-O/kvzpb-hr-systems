from django.apps import AppConfig
from django.apps import apps
from django.db import IntegrityError


class JudgmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'judgment'
    verbose_name = "Аппарат мировых судей"
