from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Carrito, Producto, ItemCarrito
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autenticar automáticamente tras el registro
            return redirect('catalogo')  # Redirige al catálogo tras registrarse
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


def agregar_al_carrito(request, producto_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')
        return redirect('login')
    
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
    else:
        item.cantidad = 1  # Asegúrate de inicializar la cantidad
    item.save()
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)
    return render(request, 'core/carrito.html', {'items': items})



@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')


def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'core/catalogo.html', {'productos': productos})


def solicitud(request):
    return render(request, 'core/solicitud.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autentica automáticamente al usuario tras el registro
            return redirect('catalogo')  # Redirige al catálogo tras registrarse
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


@login_required
def pedido(request):
    # Obtener los pedidos del usuario actual
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')  

    return render(request, 'core/pedidos.html', {'pedidos': pedidos})


@login_required
def confirmar_pago(request):
    # Obtener el carrito del usuario
    try:
        carrito = Carrito.objects.get(usuario=request.user)  
    except Carrito.DoesNotExist:
        # Si no hay carrito asociado, redirige al carrito vacío
        return redirect('carrito')

    # Verificar si el carrito no está vacío
    if not carrito.itemcarrito_set.exists():
        return redirect('carrito')  # Redirige al carrito si está vacío

    if request.method == 'POST':
        # Crear el pedido solo si no existe un pedido para este carrito
        pedido = Pedido.objects.create(
            usuario=request.user,  # Cambiado 'cliente' por 'usuario'
            carrito=carrito,  # Asociar el carrito con el pedido
            total=carrito.total,
            estado='PEND',
        )

        # Vaciar el carrito anterior
        carrito.itemcarrito_set.all().delete()

        # **No crear un nuevo carrito si ya existe uno**
        carrito.total = 0
        carrito.save()

        # Redirigir al historial de pedidos
        return redirect('pedidos_cliente')

    return render(request, 'core/confirmar.html', {'carrito': carrito})
        
        
