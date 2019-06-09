from django.contrib.gis import admin
from .models import Country, County, Constituency, Ward

# Register your models here.
admin.site.register(Country, admin.GeoModelAdmin)
admin.site.register(County, admin.GeoModelAdmin)
admin.site.register(Constituency, admin.GeoModelAdmin)
admin.site.register(Ward, admin.GeoModelAdmin)