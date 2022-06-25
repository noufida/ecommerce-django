# Generated by Django 3.2.12 on 2022-06-13 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_discountcoupon'),
        ('order', '0009_order_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.discountcoupon'),
        ),
    ]
