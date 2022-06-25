# Generated by Django 3.2.12 on 2022-06-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Failed', 'Failed'), ('Delivered', 'Delivered')], default='New', max_length=10),
        ),
    ]
