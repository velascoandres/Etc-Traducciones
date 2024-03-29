# Generated by Django 2.0.5 on 2018-08-05 04:56

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PagoPaypal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(db_index=True, max_length=64)),
                ('payer_id', models.CharField(blank=True, db_index=True, max_length=128)),
                ('payer_email', models.EmailField(blank=True, max_length=254)),
                ('precio', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('pagado', models.BooleanField(default=False)),
            ],
        ),
    ]
