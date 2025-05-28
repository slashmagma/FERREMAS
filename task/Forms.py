from django.forms import ModelForm
from .models import Categoria, articulo

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombrecat', 'descripcion', 'imagen']
        
class ArticuloForm(ModelForm):
    class Meta:
        model = articulo
        fields = ['nombreart', 'descripcion', 'imagen', 'valorunidad', 'cantidad']