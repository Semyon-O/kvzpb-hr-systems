from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from . import models
from . import serializers

# Create your views here.
class TimeUserWindowView(generics.ListAPIView):
    queryset = models.TimeUserWindow.objects.all()
    serializer_class = serializers.TimeWindowSerializer

    def list(self, request, *args, **kwargs):
        email_judge = request.query_params.get('email')
        freeTimeWindowsJudge = models.TimeUserWindow.objects.filter(Q(user__email=email_judge) & Q(status='open')).all()
        response = serializers.TimeWindowSerializer(freeTimeWindowsJudge, many=True)
        return Response(response.data, status=status.HTTP_200_OK)


class TakeTimeOrder(generics.CreateAPIView):
    queryset = models.TimeOrder.objects.all()
    serializer_class = serializers.TimeOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)