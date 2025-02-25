from django.urls import path
from rest_framework import routers

from . import api

url_router = routers.DefaultRouter()

urlpatterns = [
    path('', api.CreateNewCandidate.as_view(), name='create-candidate'),
    path('<int:tg_id>/check-status', api.CheckCandidateAccess.as_view(), name='check-status'),
]