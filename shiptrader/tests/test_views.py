from datetime import datetime, timedelta

from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from shiptrader.models import Starship, Listing


def create_starships():
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


class StarshipTestCase(APITestCase):

    def setUp(self):
        create_starships()

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


class ListingTestCase(APITestCase):

    def setUp(self):
        create_starships()

    def test_create_listing(self):
        starship = Starship.objects.first()
        response = self.client.post(
            reverse('listing-list'), format='json',
            data={'name': 'Victory', 'price': 10, 'ship_type': starship.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.all().count(), 1)
        self.assertEqual(Listing.objects.first().ship_type, starship)
        self.assertEqual(Listing.objects.first().active, True)
        self.assertLess(
            now() - Listing.objects.first().last_listed,
            timedelta(seconds=1)
        )

    def test_list_listings_by_price(self):
        starship_1 = Starship.objects.all()[0]
        starship_2 = Starship.objects.all()[1]
        Listing(name='Victory', price=10, ship_type=starship_1).save()
        Listing(name='Arrow', price=50, ship_type=starship_2).save()

        response = self.client.get(
            reverse('listing-list'), {'ordering': '-price'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Arrow'
        )
        self.assertEqual(
            response.data['results'][1]['name'],
            'Victory'
        )

    def test_list_listings_by_date(self):
        starship_1 = Starship.objects.all()[0]
        starship_2 = Starship.objects.all()[1]
        Listing(name='Victory', price=10, ship_type=starship_1).save()
        Listing(
            name='Arrow', price=50, ship_type=starship_2,
            last_listed=now() - timedelta(days=3)
        ).save()

        response = self.client.get(
            reverse('listing-list'), {'ordering': 'last_listed'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Arrow'
        )
        self.assertEqual(
            response.data['results'][1]['name'],
            'Victory'
        )

    def test_filter_listings_by_class(self):
        starship_1 = Starship.objects.all()[0]
        starship_2 = Starship.objects.all()[1]
        Listing(name='Victory', price=10, ship_type=starship_1).save()
        Listing(name='Arrow', price=50, ship_type=starship_2).save()

        response = self.client.get(
            reverse('listing-list'),
            {'starship_class': starship_1.starship_class}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Victory'
        )

    def test_deactivate_listing(self):
        starship_1 = Starship.objects.all()[0]
        listing = Listing(name='Victory', price=10, ship_type=starship_1)
        listing.save()

        response = self.client.post(
            reverse('listing-deactivate', kwargs={'pk': listing.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Listing.objects.get(pk=listing.id).active)

    def test_activate_listing(self):
        starship_1 = Starship.objects.all()[0]
        listing = Listing(
            name='Victory', price=10, ship_type=starship_1,
            active=False, last_listed=now() - timedelta(days=3)
        )
        listing.save()

        response = self.client.post(
            reverse('listing-activate', kwargs={'pk': listing.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Listing.objects.get(pk=listing.id).active)
        self.assertLess(
            now() - Listing.objects.get(pk=listing.id).last_listed,
            timedelta(seconds=1)
        )
