# Generated by Django 5.1.2 on 2025-04-07 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/default.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
