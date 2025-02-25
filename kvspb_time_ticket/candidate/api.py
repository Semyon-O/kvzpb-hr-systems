from os import access

from django.core.serializers import get_serializer
from rest_framework import generics, status
from rest_framework.response import Response

from candidate.models import Candidate, CandidateAccess
from candidate.serializers import CandidateSerializer, CandidateAccessSerializer


class CreateNewCandidate(generics.CreateAPIView):
    """
    Создает запись кандидата. При создании записи, создается также запись на проверку документов.
    Статус проверки по умолчанию ставиться в not_read (не прочитано)
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response


class CheckCandidateAccess(generics.RetrieveAPIView):
    """
    Получает информацию о ходе проверки документов кандидата.
    Три статуса:
        - not_read (Не просмотрено)
        - access (Документы приняты)
        - not_access (Документы не были посланы)
    """
    queryset = CandidateAccess.objects.all()
    serializer_class = CandidateAccessSerializer

    def retrieve(self, request, *args, **kwargs):

        tg_id = kwargs.get('tg_id')
        candidate_access = self.__retrieve_by_tg_id(tg_id)
        serializer = CandidateAccessSerializer(candidate_access, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def __retrieve_by_tg_id(self, tg_id):
        candidate = Candidate.objects.filter(telegram_id=tg_id).first()
        candidate_access = CandidateAccess.objects.filter(candidate=candidate).first()
        return candidate_access
