# Generated by Django 3.0.4 on 2020-10-31 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201031_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.CharField(default='karnataka', max_length=30),
        ),
    ]