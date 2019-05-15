from rest_framework import mixins, viewsets

from shiptrader.serializers import StarshipSerializer
from shiptrader.models import Starship


class StarshipView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Starship.objects.all().order_by('pk')
    serializer_class = StarshipSerializer
