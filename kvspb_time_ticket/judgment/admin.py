from django.contrib import admin

from judgment.models import Judgment, VacancyInJudgment, District, Vacancy

class VacancyInJudgmentInlineAdmin(admin.TabularInline):
    model = VacancyInJudgment
    extra = 3


# TODO: Сделать загрузку excel
class JudgmentAdmin(admin.ModelAdmin):
    list_display = ("id_judgment","fio_judgment", "district","inspector__first_name")
    change_list_template = "admin/judgment/judgment/judgment_change_list.html"
    inlines = [VacancyInJudgmentInlineAdmin]
    list_filter = ("id_judgment", "district", "inspector__first_name",)


class VacancyInJudgmentAdmin(admin.ModelAdmin):
    change_list_template = "admin/judgment/vacancyinjudgment/vacancy_in_judgment_change_list.html"

class VacancyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']

admin.site.register(Judgment, JudgmentAdmin)
admin.site.register(VacancyInJudgment, VacancyInJudgmentAdmin)
admin.site.register(District)
admin.site.register(Vacancy, VacancyAdmin)
