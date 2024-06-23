# Generated by Django 5.0.6 on 2024-06-23 14:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0015_documents_auto_images_auto_ip_auto_and_more'),
        ('users', '0006_alter_customuser_managers_remove_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='changed',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='images',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
