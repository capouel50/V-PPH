# Generated by Django 5.0.2 on 2024-03-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0141_remove_formule_controle_formule_controles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profil', models.JSONField()),
                ('competences', models.JSONField()),
                ('situations', models.JSONField()),
                ('personnas', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
