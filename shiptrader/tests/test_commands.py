from django.conf import settings
from django.core.management import call_command, CommandError
from django.test import TestCase
import responses

from shiptrader.models import Starship

test_data = [
    {
        'count': 2,
        'next': 'https://swapi.co/api/starships/?page=2',
        'previous': None,
        'results': [
            {
                'name': 'Executor',
                'model': 'Executor-class star dreadnought',
                'manufacturer': 'Kuat Drive Yards,Fondor Shipyards',
                'cost_in_credits': '1143350000',
                'length': '19000',
                'max_atmosphering_speed': 'n/a',
                'crew': '279144',
                'passengers': '38000',
                'cargo_capacity': '250000000',
                'consumables': '6 years',
                'hyperdrive_rating': '2.0',
                'MGLT': '40',
                'starship_class': 'Star dreadnought',
                'pilots': [],
                'films': [
                    'https://swapi.co/api/films/2/',
                    'https://swapi.co/api/films/3/'
                ],
                'created': '2014-12-15T12:31:42.547000Z',
                'edited': '2017-04-19T10:56:06.685592Z',
                'url': 'https://swapi.co/api/starships/15/'
            },
        ]
    },
    {
        'count': 2,
        'next': None,
        'previous': None,
        'results': [
            {
                "name": "Sentinel-class landing craft",
                "model": "Sentinel-class landing craft",
                "manufacturer": "Sienar Fleet Systems,Cyngus Spaceworks",
                "cost_in_credits": "240000",
                "length": "38",
                "max_atmosphering_speed": "1000",
                "crew": "5",
                "passengers": "75",
                "cargo_capacity": "180000",
                "consumables": "1 month",
                "hyperdrive_rating": "1.0",
                "MGLT": "70",
                "starship_class": "landing craft",
                "pilots": [],
                "films": [
                    "https://swapi.co/api/films/1/"
                ],
                "created": "2014-12-10T15:48:00.586000Z",
                "edited": "2014-12-22T17:35:44.431407Z",
                "url": "https://swapi.co/api/starships/5/"
            },
        ]
    }
]


class LoadStarshipsTestCase(TestCase):

    def test_starship_import(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                rsps.GET,
                settings.STARSHIP_API_PATH,
                json=test_data[0],
                match_querystring=True
            )
            rsps.add(
                rsps.GET,
                settings.STARSHIP_API_PATH + '?page=2',
                json=test_data[1],
                match_querystring=True
            )
            call_command('load_starships')
            self.assertEqual(Starship.objects.count(), 2)

    def test_starship_import_unspecified_values(self):
        altered_test_data = test_data.copy()
        altered_test_data[0]['results'][0]['cargo_capacity'] = 'unknown'
        altered_test_data[1]['results'][0]['passengers'] = 'n/a'

        with responses.RequestsMock() as rsps:
            rsps.add(
                rsps.GET,
                settings.STARSHIP_API_PATH,
                json=altered_test_data[0],
                match_querystring=True
            )
            rsps.add(
                rsps.GET,
                settings.STARSHIP_API_PATH + '?page=2',
                json=altered_test_data[1],
                match_querystring=True
            )
            call_command('load_starships')
            self.assertEqual(Starship.objects.count(), 2)
            self.assertIsNone(
                Starship.objects.all()[0].cargo_capacity
            )
            self.assertIsNone(
                Starship.objects.all()[1].passengers
            )

    def test_errors_for_empty(self):
         with responses.RequestsMock() as rsps:
            rsps.add(
                rsps.GET,
                settings.STARSHIP_API_PATH,
                json={
                    'count': 0,
                    'next': None,
                    'previous': None,
                    'results': []
                },
                match_querystring=True
            )
            with self.assertRaises(CommandError):
                call_command('load_starships')
