# Generated by Django 5.0.6 on 2024-07-06 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='call_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='lead',
            name='converted',
            field=models.BooleanField(default=False),
        ),
    ]
