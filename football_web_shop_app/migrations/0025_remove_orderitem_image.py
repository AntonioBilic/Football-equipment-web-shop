# Generated by Django 5.0.6 on 2024-06-28 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_web_shop_app', '0024_productsize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='image',
        ),
    ]
