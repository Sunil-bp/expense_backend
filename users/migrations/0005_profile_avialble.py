# Generated by Django 3.0.4 on 2020-11-02 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201031_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avialble',
            field=models.BooleanField(default=False),
        ),
    ]