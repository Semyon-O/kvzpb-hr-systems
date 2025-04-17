from rest_framework import serializers

from candidate.models import Candidate, CandidateAccess

from judgment.models import Judgment


class CandidateSerializer(serializers.ModelSerializer):
    id_judgement_place = serializers.IntegerField(write_only=True)

    class Meta:
        model = Candidate
        fields = ['name','surname', 'last_name', 'email', 'telegram_id','id_judgement_place']


    def create(self, validated_data):
        # Извлекаем id_judgement_place и удаляем его из данных кандидата
        id_judgement_place = validated_data.pop('id_judgement_place', None)

        # Создаем кандидата
        candidate = Candidate.objects.create(**validated_data)

        # Получаем объект Judgment по id (если передан)
        judgment_place = None
        if id_judgement_place:
            judgment_place = Judgment.objects.get(id_judgment=id_judgement_place)

        candidate_access = CandidateAccess.objects.create(
            candidate=candidate,
            judgment_place=judgment_place
        )
        return candidate

class CandidateAccessSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = CandidateAccess
        fields = ('candidate', 'status')