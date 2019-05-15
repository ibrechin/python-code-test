from django.conf import settings
from django.core.management import BaseCommand, CommandError
import requests

from shiptrader.models import Starship


class Command(BaseCommand):
    help = 'Loads all starship records from swapi.co'

    def add_arguments(self, parser):
        parser.add_argument('--replace', action='store_true',
                            help='Delete any existing records before loading')

    def handle(self, *args, **options):
        if options['replace']:
            Starship.objects.all().delete()

        def clean_number(value):
            if value in ('unknown', 'n/a'):
                return None
            return value.replace(',', '')

        path = settings.STARSHIP_API_PATH
        while path is not None:
            response = requests.get(path)
            if response.status_code != 200:
                raise CommandError('{} returned a response with status {}'.format(
                    path, response.status_code
                ))
            content = response.json()
            if content['count'] == 0:
                raise CommandError('No starships available for import')
            new_starships = []
            for starship in content['results']:
                new_starships.append(
                    Starship(
                        starship_class=starship['starship_class'],
                        manufacturer=starship['manufacturer'],
                        length=clean_number(starship['length']),
                        hyperdrive_rating=clean_number(starship['hyperdrive_rating']),
                        cargo_capacity=clean_number(starship['cargo_capacity']),
                        crew=clean_number(starship['crew']),
                        passengers=clean_number(starship['passengers']),
                    )
                )
            Starship.objects.bulk_create(new_starships)
            path = content['next']
