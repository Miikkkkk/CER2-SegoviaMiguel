from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to= "static/imagenes", null=True, blank=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'
    
class Pedido(models.Model):
    
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que hizo el pedido
    fecha_pedido = models.DateTimeField(auto_now_add=True)  # Fecha del pedido
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')  # Estado del pedido

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username} - {self.estado}"