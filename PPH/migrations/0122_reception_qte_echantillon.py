# Generated by Django 5.0.2 on 2024-03-02 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0121_alter_reception_echantillon'),
    ]

    operations = [
        migrations.AddField(
            model_name='reception',
            name='qte_echantillon',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
