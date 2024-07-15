# Generated by Django 5.0.6 on 2024-07-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0024_alter_images_profile_card_images_card_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='likes',
        ),
        migrations.AddField(
            model_name='like',
            name='is_liked',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
