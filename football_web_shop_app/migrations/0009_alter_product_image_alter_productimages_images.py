# Generated by Django 5.0.6 on 2024-06-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_web_shop_app', '0008_rename_paid_staus_order_paid_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
