# Generated by Django 4.0.2 on 2022-11-16 20:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Wallet',
        ),
    ]
