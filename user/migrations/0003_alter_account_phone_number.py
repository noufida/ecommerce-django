# Generated by Django 3.2.13 on 2022-05-30 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_account_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.TextField(max_length=50, unique=True),
        ),
    ]
