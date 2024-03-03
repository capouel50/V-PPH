# Generated by Django 5.0.2 on 2024-03-03 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0123_alter_reception_stock_reception'),
    ]

    operations = [
        migrations.AddField(
            model_name='balances',
            name='duree_calibration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='instructionsbalances',
            name='action',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='CompositionFiche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_fiche', models.IntegerField(null=True)),
                ('qté', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('ecart', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('resettable', models.BooleanField(default=True)),
                ('matiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.matierepremiere')),
            ],
        ),
    ]
