# Generated by Django 5.0.4 on 2024-04-11 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_predict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predict',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
