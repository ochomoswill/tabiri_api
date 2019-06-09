"""tabiri_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from tabiri_api.apps.tabiri_gis import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'countries', views.CountryViewSet)
# router.register(r'counties', views.CountyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Tabiri API', description='RESTful API for Vaccine Demand Forecasting and Visualization')),
    path('api/gis/', include('tabiri_api.apps.tabiri_gis.urls', namespace='tabiri_gis')),
]
