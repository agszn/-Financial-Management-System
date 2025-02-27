# Generated by Django 5.1.4 on 2024-12-14 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_adminnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blacklist',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='ip_address',
        ),
        migrations.AddField(
            model_name='blacklist',
            name='credit_card_number',
            field=models.CharField(default=8521463097584231, max_length=16, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='credit_card_number',
            field=models.CharField(default=5123468721548962, max_length=16),
        ),
    ]
