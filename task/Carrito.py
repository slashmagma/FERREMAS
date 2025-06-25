from decimal import Decimal
from django.contrib import messages
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session 
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    
    def agregar(self, articulo):
        id = str(articulo.id)

        # Si el artículo no está en el carrito, lo agregamos con cantidad 1
        if id not in self.carrito.keys():
            if articulo.cantidad > 0:
                self.carrito[id] = {
                    "articulo_id": articulo.id,
                    "tipo": articulo.Tipo,
                    "nombreart": articulo.nombreart,
                    "acumulado": float(articulo.valorunidad),
                    "cantidad": 1,
                    "imagen": articulo.imagen.url if articulo.imagen else None
                }
        else:
            # Ya existe en el carrito, validamos que no exceda el stock
            cantidad_actual = self.carrito[id]["cantidad"]
            if cantidad_actual < articulo.cantidad:
                self.carrito[id]["cantidad"] += 1
                self.carrito[id]["acumulado"] = float(articulo.valorunidad)
            else:
                
                  messages.warning(
            self.request,
            f"Ya agregaste todas las unidades disponibles de '{articulo.nombreart}'.")

        self.guardar_carrito()

        
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    def eliminar(self, articulo):
        id = str(articulo.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
            
    def eliminar_producto(self, articulo):
        id = str(articulo.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] = float(articulo.valorunidad)
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(articulo)
            self.guardar_carrito() 
    def eliminar_articulo(self, articulo):
        id = str(articulo.id)
        if id in self.carrito:
            cantidad_carrito = self.carrito[id]["cantidad"]
            
            # Descontar stock y guardar en base de datos
            articulo.cantidad = max(0, articulo.cantidad - cantidad_carrito)
            articulo.save()

            
    
    def limpiar_carrito(self):
        self.session["carrito"] = {}
        self.session.modified = True