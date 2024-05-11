# Generated by Django 5.0.4 on 2024-04-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_maestro_his_establecimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='DimDiscapacidadEtapa',
            fields=[
                ('EtapaKey', models.IntegerField(primary_key=True, serialize=False)),
                ('Etapa', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'DimDiscapacidadEtapa',
            },
        ),
    ]