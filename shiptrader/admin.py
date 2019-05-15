from django.contrib import admin

from shiptrader.models import Starship


@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    list_display = ('starship_class', 'manufacturer')
