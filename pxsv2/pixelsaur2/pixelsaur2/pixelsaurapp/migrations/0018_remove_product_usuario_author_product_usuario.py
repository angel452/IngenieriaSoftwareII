# Generated by Django 4.0.2 on 2022-11-21 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixelsaurapp', '0017_alter_category_options_category_level_category_lft_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='usuario_author',
        ),
        migrations.AddField(
            model_name='product',
            name='usuario',
            field=models.CharField(db_index=True, default=0, help_text='Entra el nombre del autor', max_length=200),
            preserve_default=False,
        ),
    ]