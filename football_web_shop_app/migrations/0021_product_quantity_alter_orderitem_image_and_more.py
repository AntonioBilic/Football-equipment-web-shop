# Generated by Django 5.0.6 on 2024-06-28 17:27

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_web_shop_app', '0020_user_address_user_city_user_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='image',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
