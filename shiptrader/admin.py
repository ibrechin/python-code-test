from django.contrib import admin

from shiptrader.models import Starship, Listing


@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    list_display = ('starship_class', 'manufacturer')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
