from django.contrib import admin

from judgment.models import Judgment, VacancyInJudgment, District, Vacancy

# TODO: Сделать загрузку excel
class JudgmentAdmin(admin.ModelAdmin):
    list_display = ("id_judgment","fio_judgment", "district",)

    change_list_template = "admin/judgment/judgment/judgment_change_list.html"



class VacancyInJudgmentAdmin(admin.ModelAdmin):

    change_list_template = "admin/judgment/vacancyinjudgment/vacancy_in_judgment_change_list.html"


admin.site.register(Judgment, JudgmentAdmin)
admin.site.register(VacancyInJudgment, VacancyInJudgmentAdmin)
admin.site.register(District)
admin.site.register(Vacancy)
