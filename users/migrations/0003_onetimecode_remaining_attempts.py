# Generated by Django 5.0.6 on 2024-05-31 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_bio_customuser_info_onetimecode'),
    ]

    operations = [
        migrations.AddField(
            model_name='onetimecode',
            name='remaining_attempts',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='Оставшиеся попытки'),
        ),
    ]
