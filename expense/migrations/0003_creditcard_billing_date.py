# Generated by Django 3.0.4 on 2020-11-09 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_auto_20201109_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='billing_date',
            field=models.DateField(default=datetime.datetime(2020, 11, 9, 18, 11, 33, 781578)),
            preserve_default=False,
        ),
    ]
