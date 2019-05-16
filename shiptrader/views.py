import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from rest_framework import mixins, viewsets, decorators, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

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
        fields = {
            'active': ['exact']
        }


class StableOrderingFilter(OrderingFilter):
    """
    This filter maintains a stable sort when ordering by a field
    that may have duplicate values by adding a secondary ordering
    by pk. This keeps pagination sane.
    """
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering and 'pk' not in ordering:
            return list(ordering) + ['pk']
        return ordering


class ListingView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Listing.objects.order_by('pk')
    filter_backends = (DjangoFilterBackend, StableOrderingFilter,)
    filter_class = ListingFilter
    serializer_class = ListingSerializer
    ordering_fields = ('price', 'last_listed',)

    @decorators.action(
        methods=['post'], detail=True,
        url_path='activate', url_name='activate'
    )
    def activate(self, request, pk=None):
        obj = self.get_object()
        if not obj.active:
            obj.active = True
            obj.last_listed = now()
            obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(
        methods=['post'], detail=True,
        url_path='deactivate', url_name='deactivate'
    )
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.active = False
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
