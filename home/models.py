from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Departure(models.Model):
    city_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city_name

class Delivery(models.Model):
    city_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city_name


class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    product_type = models.CharField(max_length=100)
    departure = models.ForeignKey('Departure', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)

    WEATHER_CHOICES = [
        ('Sunny', 'conditions Sunny'),
        ('Stormy', 'conditions Stormy'),
        ('Sandstorms', 'conditions Sandstorms'),
        ('Cloudy', 'conditions Cloudy'),
        ('Fog', 'conditions Fog'),
        ('Windy', 'conditions Windy'),
        ('NaN', 'conditions NaN'),
    ]
    weather_conditions = models.CharField(max_length=20, choices=WEATHER_CHOICES, default='NaN')

    MULTIPLE_DELIVERIES_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ]
    multiple_deliveries = models.IntegerField(choices=MULTIPLE_DELIVERIES_CHOICES, default=0)

    festival = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s input: {self.departure} to {self.delivery}"
