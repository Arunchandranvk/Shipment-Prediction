from django.contrib import admin
from .models import Departure, Delivery, UserInput,Predict

# Register your models here.
admin.site.register(Departure)
admin.site.register(Delivery)
admin.site.register(UserInput)
admin.site.register(Predict)
