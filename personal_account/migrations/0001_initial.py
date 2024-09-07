# Generated by Django 5.0.6 on 2024-09-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Баланс пользователя')),
                ('currency', models.CharField(choices=[('RUB', 'RUBLES'), ('USD', 'DOLLARS'), ('EUR', 'EURO')], default='RUB', max_length=3)),
            ],
            options={
                'verbose_name': 'Баланс',
                'verbose_name_plural': 'Балансы',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Сумма платежа')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED')], default='PENDING', max_length=10, verbose_name='Статус платежа')),
                ('creating_payment', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания платежа')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-creating_payment'],
            },
        ),
    ]
