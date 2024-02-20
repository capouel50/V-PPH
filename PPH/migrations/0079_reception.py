# Generated by Django 4.2.3 on 2024-02-13 16:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0078_remove_catalogue_prix_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reception', models.DateField(blank=True, default=datetime.date.today)),
                ('lot', models.CharField(max_length=200, null=True)),
                ('peremption', models.DateField(blank=True)),
                ('certificat', models.FileField(upload_to='certificats/')),
                ('qte', models.PositiveIntegerField(blank=True, null=True)),
                ('matiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.matierepremiere')),
            ],
        ),
    ]