# Generated by Django 5.0.4 on 2024-04-11 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_userinput_prediction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='multiple_deliveries',
            field=models.CharField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], max_length=100),
        ),
    ]
