# Generated by Django 3.2.12 on 2022-06-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_discountcoupon_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcoupon',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
