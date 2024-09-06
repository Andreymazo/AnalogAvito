# Generated by Django 5.0.6 on 2024-09-06 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0013_bagsknapsacks_content_type_bagsknapsacks_object_id'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='content_type',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='object_id',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
