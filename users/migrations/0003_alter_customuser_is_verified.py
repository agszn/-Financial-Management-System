# Generated by Django 5.0.3 on 2024-12-01 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_managers_customuser_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='email verified'),
        ),
    ]
