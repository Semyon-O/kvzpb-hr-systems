from django.urls import path
from rest_framework import routers

from . import api, views

url_router = routers.DefaultRouter()


urlpatterns = [
    # api.py

    path('', api.ListJudgments.as_view(), name='judgments'),
    path('<int:pk>', api.RetrieveJudgment.as_view(), name='judgment'),
    path('vacancy/types', api.ListVacancy.as_view(), name='vacancy_types'),
    path('district', api.ListDistricts.as_view(), name='districts'),

]