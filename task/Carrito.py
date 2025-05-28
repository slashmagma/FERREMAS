from decimal import Decimal
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
        id=str(articulo.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "articulo_id": articulo.id,
                "nombreart": articulo.nombreart,
                "acumulado": articulo.valorunidad,
                "cantidad": 1,
                "imagen": articulo.imagen.url if articulo.imagen else None
            }
        else:
            self.carrito[id]["cantidad"] += 1 
            self.carrito[id]["acumulado"] = articulo.valorunidad
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
            self.carrito[id]["acumulado"] = articulo.valorunidad
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(articulo)
            self.guardar_carrito()  
    
    def limpiar_carrito(self):
        self.session["carrito"] = {}
        self.session.modified = True