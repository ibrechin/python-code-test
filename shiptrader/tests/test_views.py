from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shiptrader.models import Starship


class StarshipTestCase(APITestCase):

    def setUp(self):
        Starship(
            starship_class='cruiser',
            manufacturer='SpaceX',
            length=12.5,
            hyperdrive_rating=1.3,
            cargo_capacity=1800,
            crew=3,
            passengers=4,
        ).save()
        Starship(
            starship_class='battleship',
            manufacturer='BlueOrigin',
            length=5.5,
            hyperdrive_rating=5.0,
            cargo_capacity=500,
            crew=1,
            passengers=2,
        ).save()

    def test_get_starship_list(self):
        response = self.client.get(
            reverse('starship-list'), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_starship_detail(self):
        pk = Starship.objects.first().id
        response = self.client.get(
            reverse('starship-detail', kwargs={'pk': pk}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['starship_class'], 'cruiser')