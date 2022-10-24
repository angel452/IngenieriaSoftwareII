from django.contrib import admin
from .models import contenido
from .models import Categoria
# Register your models here.
#admin.site.register(contenido)
#admin.site.register(Categoria)
@admin.register(contenido)
class contenidoAdmin(admin.ModelAdmin):
    list_display = ('name', 'precio','media_banner')

#@admin.register(Categoria)
#class CategoriaAdmin(admin.ModelAdmin):
#    pass