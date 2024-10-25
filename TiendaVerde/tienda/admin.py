from django.contrib import admin
from .models import Producto
from .models import Carrito
from .models import Pedido


# Register your models here.

admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Pedido)