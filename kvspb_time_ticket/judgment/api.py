from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from . import models, serializers, filters
from drf_yasg.inspectors import FilterInspector
from django_filters import rest_framework as rest_filters

class ListJudgments(generics.ListAPIView):
    """
    Возвращает список участков мировых судей
    """
    queryset = models.Judgment.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    def get_serializer_class(self):
        return serializers.JudgmentSerializer


class RetrieveJudgment(generics.RetrieveAPIView):
    """
    Возвращает информацию по участку мирового судьи
    """
    queryset = models.Judgment.objects.all()
    serializer_class = serializers.JudgmentSerializer


    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response


class ListVacancy(generics.ListAPIView):
    """
    Возвращает список вакансии
    """
    queryset = models.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


class ListDistricts(generics.ListAPIView):
    """
    API-handler для получения районов г. СПБ.
    Есть специальный параметр фильтрации по активным вакансиям в районах. <b>vacancy</b>
    Пример: <i>/api/judgment/district?vacancy=НОМЕР_УЧАСТКА</i>
    При использовании данного аргумента в запросе. Вернуться только те районы, в которых есть вакансии мир.суд.
    """

    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictSerializer
    filter_backends = (rest_filters.DjangoFilterBackend,)
    filterset_class = filters.DistrictsByVacanciesFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response