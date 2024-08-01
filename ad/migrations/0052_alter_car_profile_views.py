# Generated by Django 5.0.6 on 2024-07-30 19:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0051_delete_views'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0011_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='users.profile'),
        ),
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='view', to='users.profile')),
            ],
        ),
    ]
