# Generated by Django 5.0.4 on 2024-04-12 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_userinput_weather_conditions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinput',
            name='time',
        ),
        migrations.AddField(
            model_name='userinput',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
