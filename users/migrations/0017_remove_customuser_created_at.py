# Generated by Django 5.0.6 on 2024-06-08 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_customuser_banned_at_customuser_changed_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='created_at',
        ),
    ]
