# Generated by Django 5.0.1 on 2024-01-24 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_first_name_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_no',
            field=models.IntegerField(default=0),
        ),
    ]
