from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import api_root, CountryListView, CountryRetrieveView, CountyRetrieveView, \
    CountyListView, ConstituencyListView, ConstituencyRetrieveView, WardListView, WardRetrieveView, \
    HealthFacilityListView, HealthFacilityRetrieveView

app_name = 'tabiri_gis'

urlpatterns = [
    path('countries', CountryListView.as_view(), name='countries-list'),
    path('countries/<str:adm0_pcode>', CountryRetrieveView.as_view(), name='country-detail'),

    path('counties', CountyListView.as_view(), name='counties-list'),
    path('counties/<str:county_cod>', CountyRetrieveView.as_view(), name='county-detail'),

    path('constituencies', ConstituencyListView.as_view(), name='constituencies-list'),
    path('constituencies/<str:const_code>', ConstituencyRetrieveView.as_view(), name='constituency-detail'),

    path('wards', WardListView.as_view(), name='wards-list'),
    path('wards/<str:objectid>', WardRetrieveView.as_view(), name='ward-detail'),

    path('health-facilities', HealthFacilityListView.as_view(), name='health-facilities-list'),
    path('health-facilities/<str:orgunitid>', HealthFacilityRetrieveView.as_view(), name='health-facility-detail'),
    path('', api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])