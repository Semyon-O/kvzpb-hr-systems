from django.contrib import admin

from judgment.models import Judgment, VacancyInJudgment, District, Vacancy

# TODO: Сделать загрузку excel
class JudgmentAdmin(admin.ModelAdmin):
    list_display = ("id_judgment","fio_judgment", "district",)



admin.site.register(Judgment, JudgmentAdmin)
admin.site.register(VacancyInJudgment)
admin.site.register(District)
admin.site.register(Vacancy)
