# Generated by Django 3.2.12 on 2022-06-14 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_discountcoupon_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcoupon',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
