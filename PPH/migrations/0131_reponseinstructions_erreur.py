# Generated by Django 5.0.2 on 2024-03-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0130_remove_instructionsappareils_reponse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reponseinstructions',
            name='erreur',
            field=models.BooleanField(default=False),
        ),
    ]
