from django.contrib import admin
from .models import Product,Category
from mptt.admin import DraggableMPTTAdmin

#LISTADO de elementos en admin

"""
class AccountInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'Users'
admin.site.unregister(User)
admin.site.register(User, """
"""
 """
class CategoryAdmin(DraggableMPTTAdmin):
    pass

admin.site.register(Category, CategoryAdmin )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category' ,  'price', 'created', ]
    list_filter = ['available', 'created', 'category']
    #list_editable = ['price', 'available']
    search_fields=['name']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10