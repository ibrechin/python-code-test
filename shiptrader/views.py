import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter

from shiptrader.serializers import StarshipSerializer, ListingSerializer
from shiptrader.models import Starship, Listing


class StarshipView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Starship.objects.all().order_by('pk')
    serializer_class = StarshipSerializer


class ListingFilter(django_filters.FilterSet):
    starship_class = django_filters.CharFilter(
        field_name='ship_type__starship_class'
    )    

    class Meta:
        model = Listing
        fields = {}

class SafeOrderingFilter(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering and 'id' not in ordering:
            return list(ordering) + ['id']
        return ordering

class ListingView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Listing.objects.filter(active=True).order_by('pk')
    filter_backends = (DjangoFilterBackend, SafeOrderingFilter,)
    filter_class = ListingFilter
    serializer_class = ListingSerializer
    ordering_fields = ('price', 'last_listed',)
