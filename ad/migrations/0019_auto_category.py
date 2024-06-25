# Generated by Django 5.0.6 on 2024-06-25 08:52

import django.db.models.deletion
import mptt.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0018_alter_auto_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='category',
            field=mptt.fields.TreeForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='advertisement', to='ad.category'),
            preserve_default=False,
        ),
    ]
