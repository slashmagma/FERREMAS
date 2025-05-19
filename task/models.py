from django.db import models

# Create your models here.
class articulo(models.Model):
    Tipo = models.CharField(max_length=100)
    nombreart = models.CharField(max_length=100)
    contenido = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='articulosimg/')
    valorunidad = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nombreart + ' - por ' + self.user.username

class categoria(models.Model):
    nombrecat = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='Categoriasimg/')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE , null=True)
    def __str__(self):
        return self.nombrecat + ' - por ' + self.user.username