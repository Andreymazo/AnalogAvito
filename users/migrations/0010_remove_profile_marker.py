# Generated by Django 5.0.6 on 2024-07-25 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='marker',
        ),
    ]
