# Generated by Django 5.0.4 on 2024-04-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_predict_shipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='weather_conditions',
            field=models.CharField(choices=[(5, '5'), (4, '4'), (3, '3'), (0, '0'), (1, '1'), (6, '6'), (7, '7')], max_length=20),
        ),
    ]
