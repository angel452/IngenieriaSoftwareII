from audioop import reverse
from email.policy import default
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.

from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.contrib.auth.models import User 

# Create your models here. aqui subimos contenido, falta
class categoria(models.Model):
    name = models.CharField(max_length=200,help_text="Entra el tipo de categoria (e.g )")
    def __str__(self):
        "aqui representamos el objeto modelo"
        return self.name
#admin saldo, calificaciones, contenido, 

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class contenido(models.Model):
    name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto")
    author_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)#confirmar si esto esta correcto.
    media = models.FileField(upload_to=user_directory_path, blank=True, null=True,storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    descripcion = models.CharField()
    precio = models.DecimalField(max_digits=100,decimal_places=2,default=99.99,null=True,blank=True)
    promocion = models.DecimalField(max_digits=100, decimal_places=2, default=99.99, null=True, blank=True)
    fecha_inicio=models.DateField(null=True,blank=True)
    fecha_fin=models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['name','author_name']

     

    def __str__(self):
        return self.name

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = contenido.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return 


def product_pre_save_db(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_db, sender=contenido)

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)

