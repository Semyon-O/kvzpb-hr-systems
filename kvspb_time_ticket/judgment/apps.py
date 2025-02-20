from django.apps import AppConfig
from django.apps import apps
from django.db import IntegrityError


class JudgmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'judgment'


    def ready(self):
        # self.__create_inspector_group()
        super().ready()

   # def __create_inspector_group(self):
   #     if self.models.get('inspector', False):
   #         auth_app = apps.get_app_config('auth')
   #         Group = auth_app.get_model('Group')
   #         try:
   #             Group.objects.create(name='Inspector')
   #         except IntegrityError:
   #             print('Inspector Group already exists')