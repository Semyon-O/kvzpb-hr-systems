from django.urls import path
from . import api


url_paths = [
    path('', api.CreateNewCandidate.as_view(), name='create-candidate'),

]