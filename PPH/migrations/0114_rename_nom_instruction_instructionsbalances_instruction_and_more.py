# Generated by Django 4.2.3 on 2024-02-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0113_balances_bloque_calibration_balances_calibration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instructionsbalances',
            old_name='nom_instruction',
            new_name='instruction',
        ),
        migrations.RemoveField(
            model_name='instructionsbalances',
            name='reponse_instruction',
        ),
        migrations.RemoveField(
            model_name='instructionsbalances',
            name='valeur_instruction',
        ),
        migrations.AddField(
            model_name='instructionsbalances',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
