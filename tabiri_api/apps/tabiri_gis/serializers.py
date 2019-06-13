from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.serializers import ModelSerializer

from .models import Country, County, Constituency, Ward, HealthFacility
from rest_framework_gis.serializers import GeoFeatureModelSerializer


# Country
class CountrySerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Country
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('adm0_pcode', 'adm0_en', 'shape_leng', 'shape_area', 'date')


class CountryDetailSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Country
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('adm0_pcode', 'adm0_en', 'shape_leng', 'shape_area', 'date', 'geom')


# County
class CountySerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = County
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('county_cod', 'county_nam', 'shape_leng', 'shape_area', 'geom')


class CountyDetailSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = County
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('county_cod', 'county_nam', 'shape_leng', 'shape_area', 'geom')


# Constituency
class ConstituencySerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Constituency
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('const_code', 'constituen', 'shape_leng', 'shape_area', 'geom')


class ConstituencyDetailSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Constituency
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('const_code', 'constituen', 'shape_leng', 'shape_area', 'geom')


# Ward
class WardSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Ward
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('objectid', 'name', 'shape_leng', 'shape_area', 'geom','ward_dhis2_id')


class WardDetailSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = Ward
        geo_field = 'geom'
        auto_bbox = True
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('objectid', 'name', 'shape_leng', 'shape_area', 'geom', 'ward_dhis2_id')


# HealthFacility
class HealthFacilitySerializer(ModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = HealthFacility
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('orgunitid', 'orgunitname', 'dhis2parentid', 'dhis2id', 'lat', 'long')


class HealthFacilityDetailSerializer(ModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    class Meta:
        model = HealthFacility
        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('orgunitid', 'orgunitname', 'dhis2parentid', 'dhis2id', 'lat', 'long')