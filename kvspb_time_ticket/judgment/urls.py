from django.urls import path
from rest_framework import routers

from . import api

url_router = routers.DefaultRouter()


urlpatterns = [
    path('', api.ListJudgments.as_view(), name='judgments'),
    path('<int:pk>', api.RetrieveJudgment.as_view(), name='judgment'),
    path('vacancy/types', api.ListVacancy.as_view(), name='vacancy_types'),


]