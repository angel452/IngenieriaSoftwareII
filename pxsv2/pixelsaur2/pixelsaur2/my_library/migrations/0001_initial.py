# Generated by Django 4.0.2 on 2022-11-18 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_remove_order_address_remove_order_city_and_more'),
        ('pixelsaurapp', '0017_alter_category_options_category_level_category_lft_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBuyedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Entra el nombre de tu producto', max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(help_text='Entra una descripcion del contenido', max_length=1000)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=99.99, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='contenidos/%Y/%m/%d')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('valid_download', models.BooleanField(default=False)),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pixelsaurapp.category')),
                ('ordenid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.orderitem')),
                ('usuario_comprador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
                'index_together': {('id', 'slug')},
            },
        ),
    ]