from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.reverse import reverse

from tabiri_api.apps.tabiri_gis.exceptions import CountyDoesNotExist, CountryDoesNotExist, ConstituencyDoesNotExist, \
    WardDoesNotExist, HealthFacilityDoesNotExist
from tabiri_api.apps.tabiri_gis.renderers import CountyJSONRenderer, CountryJSONRenderer, \
    CountriesJSONRenderer, CountiesJSONRenderer, ConstituenciesJSONRenderer, ConstituencyJSONRenderer, \
    WardsJSONRenderer, WardJSONRenderer, HealthFacilitiesJSONRenderer
from .serializers import CountrySerializer, CountySerializer, ConstituencySerializer, WardSerializer, \
    HealthFacilitySerializer
from .models import Country, County, Constituency, Ward, HealthFacility
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'countries': reverse('tabiri_gis:countries-list', request=request, format=format),
        # 'country': reverse('tabiri_gis:country-detail', request=request, format=format),
        'counties': reverse('tabiri_gis:counties-list', request=request, format=format),
        # 'county': reverse('tabiri_gis:county-detail', request=request, format=format),
        'wards': reverse('tabiri_gis:wards-list', request=request, format=format),
        # 'county': reverse('tabiri_gis:county-detail', request=request, format=format),
        #'health-facilities': reverse('tabiri_gis:health-facilities-list', request=request, format=format),
        # 'county': reverse('tabiri_gis:county-detail', request=request, format=format),
    })


# Country
class CountryListView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    renderer_classes = (CountriesJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True


class CountryRetrieveView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    renderer_classes = (CountryJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def retrieve(self, request, adm0_pcode, *args, **kwargs):
        # Try to retrieve the requested profile and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            country = Country.objects.get(adm0_pcode=adm0_pcode)
        except Country.DoesNotExist:
            raise CountryDoesNotExist

        serializer = self.serializer_class(country)

        return Response(serializer.data, status=status.HTTP_200_OK)


# County
class CountyListView(ListAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    renderer_classes = (CountiesJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True


class CountyRetrieveView(RetrieveAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    renderer_classes = (CountyJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def retrieve(self, request, county_cod, *args, **kwargs):
        # Try to retrieve the requested cou and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            county = County.objects.get(county_cod=county_cod)
        except County.DoesNotExist:
            raise CountyDoesNotExist

        serializer = self.serializer_class(county)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Constituency
class ConstituencyListView(ListAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    renderer_classes = (ConstituenciesJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Constituency.objects.all()
        county_cod = self.request.query_params.get('county_cod', None)
        if county_cod is not None:
            queryset = queryset.filter(county_cod=county_cod)
        return queryset


class ConstituencyRetrieveView(RetrieveAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    renderer_classes = (ConstituencyJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def retrieve(self, request, const_code, *args, **kwargs):
        # Try to retrieve the requested cou and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            constituency = Constituency.objects.get(const_code=const_code)
        except Constituency.DoesNotExist:
            raise ConstituencyDoesNotExist

        serializer = self.serializer_class(constituency)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Ward
class WardListView(ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    renderer_classes = (WardsJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Ward.objects.all()
        const_code = self.request.query_params.get('const_code', None)
        if const_code is not None:
            queryset = queryset.filter(const_code=const_code)
        return queryset


class WardRetrieveView(RetrieveAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    renderer_classes = (WardJSONRenderer,)
    distance_filter_field = 'geometry'
    filter_backends = (DistanceToPointFilter,)
    bbox_filter_include_overlapping = True

    def retrieve(self, request, objectid, *args, **kwargs):
        # Try to retrieve the requested cou and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            ward = Ward.objects.get(objectid=objectid)
        except Ward.DoesNotExist:
            raise WardDoesNotExist

        serializer = self.serializer_class(ward)

        return Response(serializer.data, status=status.HTTP_200_OK)


# HealthFacility
class HealthFacilityListView(ListAPIView):
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = HealthFacility.objects.all()
        print(queryset)
        dhis2parentid = self.request.query_params.get('dhis2parentid', None)
        if dhis2parentid is not None:
            queryset = queryset.filter(dhis2parentid=dhis2parentid)
        return queryset


class HealthFacilityRetrieveView(RetrieveAPIView):
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer
    renderer_classes = (HealthFacilitiesJSONRenderer,)

    def retrieve(self, request, orgunitid, *args, **kwargs):
        # Try to retrieve the requested cou and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            health_facility = HealthFacility.objects.get(orgunitid=orgunitid)
        except HealthFacility.DoesNotExist:
            raise HealthFacilityDoesNotExist

        serializer = self.serializer_class(health_facility)

        return Response(serializer.data, status=status.HTTP_200_OK)