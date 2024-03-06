from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from venue.models import (
    Venue,
    KitchenType,
    VenueBusinessTime,
    VenueRating,
    UserFavoriteVenue,
)


class VenueModelAdmin(GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 9,
            "default_lat": 52.237049,
            "default_lon": 20.017532,
            "map_height": 500,
        }
    }


admin.site.register(Venue, VenueModelAdmin)
admin.site.register(KitchenType)
admin.site.register(VenueBusinessTime)
admin.site.register(VenueRating)
admin.site.register(UserFavoriteVenue)
