# Generated by Django 5.0.2 on 2024-03-01 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0120_reception_echantillon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reception',
            name='echantillon',
            field=models.BooleanField(default=False),
        ),
    ]
