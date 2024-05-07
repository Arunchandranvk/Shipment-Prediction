# Generated by Django 5.0.4 on 2024-04-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_userinput_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinput',
            name='prediction',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userinput',
            name='weather_conditions',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=20),
        ),
    ]