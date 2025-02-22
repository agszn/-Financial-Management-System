# Generated by Django 5.0.3 on 2024-12-01 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]
