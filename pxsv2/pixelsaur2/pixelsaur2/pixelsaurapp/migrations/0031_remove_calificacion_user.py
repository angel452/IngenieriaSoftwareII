# Generated by Django 4.0.2 on 2022-11-26 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pixelsaurapp', '0030_calificacion_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calificacion',
            name='user',
        ),
    ]
