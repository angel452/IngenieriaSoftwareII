from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields=['name']
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category' ,  'price', 'created', ]
    list_filter = ['available', 'created', 'category']
    #list_editable = ['price', 'available']
    search_fields=['name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10