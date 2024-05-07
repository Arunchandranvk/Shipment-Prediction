from django.contrib.auth.models import User
from django.db import models
import random

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
    # img=models.FileField(upload_to="shipment_images",null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    product_type = models.CharField(max_length=100)
    departure = models.ForeignKey('Departure', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True,null=True)
    expected_date=models.DateTimeField(null=True)
    WEATHER_CHOICES = [
        
        (5, '5'),
        (4, '4'),
        
        (0, '0'),
        (1,'1'),
        
        (6, '6'),
        (7, '7'),
        
        
    ]
    weather_conditions = models.CharField(max_length=20, choices=WEATHER_CHOICES)

    MULTIPLE_DELIVERIES_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ]
    multiple_deliveries = models.CharField(max_length=100,choices=MULTIPLE_DELIVERIES_CHOICES)

    festival = models.BooleanField(default=False)
    prediction = models.CharField(max_length=100,null=True)
    STATUS_CHOICES = (
        ('Order Confirmed','Order Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Order Confirmed')
    order_no=models.CharField(max_length=100,null=True)
    def save(self, *args, **kwargs):
        # Set weather_conditions randomly
        self.weather_conditions = random.choice([choice[0] for choice in self.WEATHER_CHOICES])
        # Set multiple_deliveries randomly
        self.multiple_deliveries = random.choice([choice[0] for choice in self.MULTIPLE_DELIVERIES_CHOICES])
        # Call the original save method to save the instance
        # self.festival = random.choice([0,1])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s input: {self.departure} to {self.delivery}"




class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    message=models.TextField()
    def __str__(self) :
        return self.Name


class Predict(models.Model):
    prediction=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    shipment=models.CharField(max_length=100,unique=True)
    # userinput=models.ForeignKey(UserInput,on_delete=models.CASCADE,related_name='user')



