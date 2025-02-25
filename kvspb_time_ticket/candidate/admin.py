from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = ('name', 'surname', 'email')
    search_fields = ('name', 'surname', 'email')


@admin.register(models.CandidateAccess)
class CandidateAccess(admin.ModelAdmin):

    list_display = ('candidate', 'status')
