# Generated by Django 5.0.4 on 2024-04-11 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='multiple_deliveries',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='userinput',
            name='weather_conditions',
            field=models.CharField(choices=[('Sunny', 'conditions Sunny'), ('Stormy', 'conditions Stormy'), ('Sandstorms', 'conditions Sandstorms'), ('Cloudy', 'conditions Cloudy'), ('Fog', 'conditions Fog'), ('Windy', 'conditions Windy'), ('NaN', 'conditions NaN')], max_length=20),
        ),
    ]
