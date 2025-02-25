from django.urls import path
from rest_framework import routers

from . import api

url_router = routers.DefaultRouter()

url_paths = [
    path('', api.CreateNewCandidate.as_view(), name='create-candidate'),
    path('<int:tg_id>/check-status', api.CheckCandidateAccess.as_view(), name='check-status'),

]