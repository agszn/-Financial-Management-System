# Generated by Django 5.0.3 on 2024-12-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
