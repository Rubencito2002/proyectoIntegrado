# Generated by Django 5.0.3 on 2024-05-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaApp', '0006_alter_ordencompraproducto_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordencompraproducto',
            name='fecha',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
