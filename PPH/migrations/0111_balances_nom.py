# Generated by Django 4.2.3 on 2024-02-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0110_matierepremiere_densite'),
    ]

    operations = [
        migrations.AddField(
            model_name='balances',
            name='nom',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
