# Generated by Django 5.0.6 on 2024-08-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0052_alter_car_profile_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photos',
            field=models.ManyToManyField(blank=True, to='ad.images'),
        ),
    ]
