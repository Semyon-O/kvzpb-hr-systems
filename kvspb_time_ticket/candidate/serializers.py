from rest_framework import serializers

from candidate.models import Candidate, CandidateAccess


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

    def create(self, validated_data):
        candidate = Candidate.objects.create(**validated_data)
        candidate.save()

        candidate_access = CandidateAccess.objects.create(candidate=candidate)
        candidate_access.save()
        return candidate


class CandidateAccessSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateAccess
        fields = ('candidate', 'status')