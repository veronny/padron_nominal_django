# Generated by Django 5.0.4 on 2024-08-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discapacidad', '0014_actualizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualizacion',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actualizacion',
            name='hora',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
