# Generated by Django 4.0.2 on 2022-12-02 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_merge_0003_profile_0004_wallet_peticion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='money',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]