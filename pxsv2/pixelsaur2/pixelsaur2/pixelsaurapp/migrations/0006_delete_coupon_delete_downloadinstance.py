# Generated by Django 4.1.2 on 2022-10-26 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pixelsaurapp', '0005_coupon'),
    ]

    operations = [
        migrations.DeleteModel(
            name='coupon',
        ),
        migrations.DeleteModel(
            name='downloadInstance',
        ),
    ]
