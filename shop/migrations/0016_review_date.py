# Generated by Django 3.1.3 on 2020-12-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_remove_review_store_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(default='2020-12-09 19:35'),
            preserve_default=False,
        ),
    ]
