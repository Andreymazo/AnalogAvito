# Generated by Django 5.0.6 on 2024-09-09 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bagsknapsacks',
            name='category',
        ),
        migrations.RemoveField(
            model_name='childclothesshoes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='menclothes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='menshoes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='wemenclothes',
            name='category',
        ),
        migrations.RemoveField(
            model_name='wemenshoes',
            name='category',
        ),
    ]
