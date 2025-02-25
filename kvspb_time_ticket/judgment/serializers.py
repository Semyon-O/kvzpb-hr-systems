from rest_framework import serializers

from judgment.models import Judgment, Vacancy, District


class JudgmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Judgment
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
