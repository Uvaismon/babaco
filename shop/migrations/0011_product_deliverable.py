# Generated by Django 3.1.3 on 2020-12-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201130_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deliverable',
            field=models.BooleanField(default=False),
        ),
    ]
