from rest_framework import serializers

from candidate.models import Candidate, CandidateAccess


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateAccessSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateAccess
        fields = ('candidate', 'status')