# Generated by Django 5.0.2 on 2024-03-08 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0137_remove_controles_type_controle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typecontrole',
            name='description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.etapes'),
        ),
        migrations.AlterField(
            model_name='typecontrole',
            name='type_appareil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.typeappareil'),
        ),
    ]
