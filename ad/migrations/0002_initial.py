# Generated by Django 5.0.6 on 2024-10-02 11:10

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ad', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='images',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='images',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='users.profile'),
        ),
        migrations.AddField(
            model_name='ip',
            name='auto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.car'),
        ),
        migrations.AddField(
            model_name='ip',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menclothes',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menclothes', to='ad.category'),
        ),
        migrations.AddField(
            model_name='menclothes',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='menshoes',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menshoes', to='ad.category'),
        ),
        migrations.AddField(
            model_name='menshoes',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='views',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='views',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='view', to='users.profile'),
        ),
        migrations.AddField(
            model_name='wemenclothes',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wemenclothes', to='ad.category'),
        ),
        migrations.AddField(
            model_name='wemenclothes',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='wemenshoes',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wemenshoes', to='ad.category'),
        ),
        migrations.AddField(
            model_name='wemenshoes',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
