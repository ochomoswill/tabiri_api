from django.db import models
from django.contrib.gis.db import models as gis_models


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)


class AdminUnitValidityModel(TimestampedModel):
    class Meta:
        abstract = True

    validon = gis_models.DateField(null=True)
    validto = gis_models.DateField(null=True)


class CountryRelatedModel(AdminUnitValidityModel):
    class Meta:
        abstract = True

    adm0_en = gis_models.CharField(max_length=50, db_column='country_name')
    adm0_pcode = gis_models.CharField(max_length=50, db_column='country_code')


class CountyRelatedModel(CountryRelatedModel):
    class Meta:
        abstract = True

    adm1_en = gis_models.CharField(max_length=50, db_column='county_name')
    adm1_pcode = gis_models.CharField(max_length=50, db_column='county_code')

