# Generated by Django 5.0.6 on 2024-06-12 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_web_shop_app', '0010_alter_productimages_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='football_web_shop_app.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='size',
            name='size_type',
            field=models.CharField(choices=[('NUM', 'Numerical'), ('CAT', 'Categorical')], max_length=20),
        ),
    ]