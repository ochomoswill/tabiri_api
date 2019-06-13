from tabiri_api.apps.core.renderers import TabiriAPIJSONRenderer


# Country
class CountriesJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'countries'


class CountryJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'country'


# County
class CountiesJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'counties'


class CountyJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'county'


# Constituency
class ConstituenciesJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'constituencies'


class ConstituencyJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'constituency'


# Ward
class WardsJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'wards'


class WardJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'ward'


# HealthFacility
class HealthFacilitiesJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'health_facilities'


class HealthFacilityJSONRenderer(TabiriAPIJSONRenderer):
    object_label = 'health_facility'