from rest_framework import generics
from . import models, serializers


# Create your views here.


class ListJudgments(generics.ListAPIView):
    # TODO: Возвращает список судейских участков
    #  Сделать фильтр по району и вакансии
    queryset = models.Judgment.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    def get_serializer_class(self):
        return serializers.JudgmentSerializer


class RetrieveJudgment(generics.RetrieveAPIView):
    queryset = models.Judgment.objects.all()
    serializer_class = serializers.JudgmentSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return response


class ListVacancy(generics.ListAPIView):
    queryset = models.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


