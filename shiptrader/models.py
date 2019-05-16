from django.db import models
from django.utils.timezone import now


class Starship(models.Model):
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    length = models.FloatField(blank=True, null=True)
    hyperdrive_rating = models.FloatField(blank=True, null=True)
    cargo_capacity = models.BigIntegerField(blank=True, null=True)

    crew = models.IntegerField(blank=True, null=True)
    passengers = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}: {}, {}'.format(self.pk, self.manufacturer, self.starship_class)


class Listing(models.Model):
    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    last_listed = models.DateTimeField(default=now)

    def __str__(self):
        return '{}: {}, {}'.format(self.pk, self.name, self.price)
