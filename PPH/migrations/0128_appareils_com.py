# Generated by Django 5.0.2 on 2024-03-04 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0127_typeappareil_typecommunication_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appareils',
            name='com',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.typecommunication'),
        ),
    ]
