# Generated by Django 5.0.6 on 2024-05-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_web_shop_app', '0002_remove_user_address_address_productdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
