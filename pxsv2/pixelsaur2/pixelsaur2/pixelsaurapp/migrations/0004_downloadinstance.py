# Generated by Django 4.1.2 on 2022-10-24 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixelsaurapp', '0003_contenido_id_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='downloadInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]