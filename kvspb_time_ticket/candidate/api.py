from rest_framework import generics

from candidate.models import Candidate
from candidate.serializers import CandidateSerializer, CandidateAccessSerializer


class CreateNewCandidate(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def create(self, request, *args, **kwargs):
        #TODO: При создании записи Кандидата, создавать запись на проверку
        response = super().create(request, *args, **kwargs)
        return response


class CheckCandidateStatus(generics.RetrieveUpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateAccessSerializer

    def retrieve(self, request, *args, **kwargs):
        # TODO: Сделать получение кандидата по TG ID
        response = super().retrieve(request, *args, **kwargs)
        return response