# Generated by Django 5.0.6 on 2024-08-24 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mssg',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
