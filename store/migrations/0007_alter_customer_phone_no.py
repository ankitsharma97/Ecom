# Generated by Django 5.0.1 on 2024-01-25 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customer_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_no',
            field=models.CharField(max_length=15),
        ),
    ]
