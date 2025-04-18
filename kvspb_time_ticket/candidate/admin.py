from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = ('name', 'surname', 'last_name', 'email',)
    search_fields = ('name', 'surname', 'last_name','email')


@admin.register(models.CandidateAccess)
class CandidateAccess(admin.ModelAdmin):

    list_display = ('candidate', 'judgment_place', 'judgment_place__inspector__first_name', 'status', 'message_to_candidate')

    search_fields = [
        'candidate__name',  # Поиск по имени кандидата
        'candidate__surname',  # Поиск по фамилии кандидата
        'candidate__email',  # Поиск по email кандидата
        'status',  # Поиск по статусу (если нужно)
    ]
    list_filter = ('status', 'judgment_place', 'judgment_place__inspector__first_name')  # Фильтр по статусу (опционально)