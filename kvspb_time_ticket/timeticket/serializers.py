from rest_framework import serializers

from . import models
from .models import TimeOrder


class TimeWindowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TimeUserWindow
        fields = '__all__'
        read_only_fields = ('status',)


class TimeOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TimeOrder
        fields = '__all__'

    def save(self, **kwargs):
        print(self, kwargs)
        new_instance: TimeOrder = super().save(**kwargs)
        self.__change_status_time_window(new_instance)
        return new_instance

    def __change_status_time_window(self, instance: TimeOrder):
        instance.taken_time.status = 'close'
        instance.taken_time.save()