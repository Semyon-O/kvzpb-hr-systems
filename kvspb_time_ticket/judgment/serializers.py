from django.contrib.auth.models import User
from rest_framework import serializers

from judgment.models import Judgment, Vacancy, District


class InspectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)


class JudgmentSerializer(serializers.ModelSerializer):
    inspector = InspectorSerializer(many=False)

    class Meta:
        model = Judgment
        fields = ("id_judgment", "district", "fio_judgment",
                  "phone", "description", "inspector", "vacancies")


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
