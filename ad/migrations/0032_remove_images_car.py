# Generated by Django 5.0.6 on 2024-07-24 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0031_promotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='car',
        ),
    ]
