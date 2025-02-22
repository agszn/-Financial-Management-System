# Generated by Django 5.0.3 on 2024-12-02 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='monthly_budget',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
