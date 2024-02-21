# Generated by Django 4.2.3 on 2024-02-21 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0112_alter_epi_nom'),
    ]

    operations = [
        migrations.AddField(
            model_name='balances',
            name='bloque_calibration',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='balances',
            name='calibration',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
