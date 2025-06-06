"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import_tools:  from my_app import_tools views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import_tools:  from other_app.views import_tools Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import_tools include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import permissions

from timeticket import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API для найма кандидатов в аппарат мировых судей",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="orekhovsemyon@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from judgment import views as judgment_views

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    # path('api/free-time-windows', views.TimeUserWindowView.as_view(), name='free-time-windows'),
    # path('api/take-time-windows', views.TakeTimeOrder.as_view(), name='take-time-windows'),
    path('api/judgment/', include('judgment.urls')),
    path('api/candidate/', include('candidate.urls')),

    # Admin Panel
    path('import_data', judgment_views.ImportJudgmentView.as_view(), name='import'),
    path('import_data_vacancies', judgment_views.ImportVacanciesInJudgmentView.as_view(), name='import_data_vacancies'),

]



