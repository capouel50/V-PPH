# Generated by Django 4.2.3 on 2024-01-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0049_demandes_commentaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandes',
            name='commentaire',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
