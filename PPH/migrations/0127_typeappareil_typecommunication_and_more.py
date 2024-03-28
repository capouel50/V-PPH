# Generated by Django 5.0.2 on 2024-03-04 14:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0126_balances_prochaine'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeAppareil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCommunication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='instructionsbalances',
            name='modele_balance',
        ),
        migrations.RenameModel(
            old_name='FabricantsBalances',
            new_name='FabricantsAppareils',
        ),
        migrations.CreateModel(
            name='Appareils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True, unique=True)),
                ('modele', models.CharField(max_length=100, unique=True)),
                ('calibration', models.DateField(blank=True, default=datetime.date.today)),
                ('duree_calibration', models.IntegerField(null=True)),
                ('prochaine', models.DateField(blank=True, null=True)),
                ('bloque_calibration', models.BooleanField(default=True)),
                ('is_activate', models.BooleanField(default=True)),
                ('fabricant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.fabricantsappareils')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.typeappareil')),
            ],
            options={
                'ordering': ['modele'],
            },
        ),
        migrations.CreateModel(
            name='InstructionsAppareils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('instruction', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('format_reponse', models.CharField(max_length=100, null=True)),
                ('modele_appareil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.appareils')),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.DeleteModel(
            name='Balances',
        ),
        migrations.DeleteModel(
            name='InstructionsBalances',
        ),
    ]