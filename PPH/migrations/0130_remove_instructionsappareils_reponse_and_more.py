# Generated by Django 5.0.2 on 2024-03-04 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0129_reponseinstructions_instructionsappareils_reponse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructionsappareils',
            name='reponse',
        ),
        migrations.AddField(
            model_name='reponseinstructions',
            name='num_instruction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.instructionsappareils'),
        ),
    ]
