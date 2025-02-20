from django.contrib import admin

from judgment.models import Judgment, VacancyInJudgment, District, Vacancy

# Register your models here.

admin.site.register(Judgment)
admin.site.register(VacancyInJudgment)
admin.site.register(District)
admin.site.register(Vacancy)
