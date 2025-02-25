from django.db.models import F
from django_filters import rest_framework as filters

from . import models


class DistrictsByVacanciesFilter(filters.FilterSet):
    vacancy = filters.ModelMultipleChoiceFilter(
        queryset=models.Vacancy.objects.all(),

    )

    class Meta:
        model = models.District
        fields = ['vacancy']


    def filter_queryset(self, queryset):
        if self.request.query_params.get('vacancy'):
            vacancy_id = self.request.query_params.get('vacancy')
            vacancy_object = models.Vacancy.objects.get(pk=vacancy_id)
            judgments_by_vacancy = models.VacancyInJudgment.objects.filter(vacancy=vacancy_object)
            districts = judgments_by_vacancy.values("judgment__district_id").distinct()

            districts_annotated = districts.annotate(name=F("judgment__district_id"))
            return districts_annotated
        return queryset
