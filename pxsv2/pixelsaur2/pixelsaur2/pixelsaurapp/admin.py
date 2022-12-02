from django.contrib import admin
from .models import Product,Category
from mptt.admin import DraggableMPTTAdmin

#LISTADO de elementos en admin

class CategoryAdmin(DraggableMPTTAdmin):
    pass

admin.site.register(Category, CategoryAdmin )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category' ,  'price', 'created', ]
    list_filter = ['available', 'created', 'category']
    search_fields=['name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10