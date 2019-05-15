from rest_framework import serializers

from shiptrader.models import Starship, Listing


class StarshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Starship
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('last_listed', 'active',)
