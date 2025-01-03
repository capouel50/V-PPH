# Generated by Django 5.0.2 on 2024-03-05 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0131_reponseinstructions_erreur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etapes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(null=True)),
                ('nom', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('resettable', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='formule',
            name='specialite',
        ),
        migrations.CreateModel(
            name='Controles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('resettable', models.BooleanField(default=True)),
                ('appareil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.matierepremiere')),
                ('type_appareil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.typeappareil')),
            ],
        ),
        migrations.AddField(
            model_name='formule',
            name='controle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.controles'),
        ),
    ]
