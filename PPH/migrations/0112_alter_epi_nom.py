# Generated by Django 4.2.3 on 2024-02-21 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0111_balances_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epi',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
