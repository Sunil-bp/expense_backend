# Generated by Django 3.0.4 on 2020-10-31 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.FileField(default='profile_pics/user_default.png', upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.CharField(max_length=30),
        ),
    ]
