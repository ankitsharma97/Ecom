# Generated by Django 5.0.1 on 2024-01-28 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(default=0),
        ),
    ]
