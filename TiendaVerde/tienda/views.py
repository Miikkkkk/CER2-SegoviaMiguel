from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Carrito, Producto
from django.shortcuts import get_object_or_404

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
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
    carrito.cantidad += 1
    carrito.save()
    return redirect('ver_carrito')


def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito)
    return render(request, 'ver_carrito.html', {'carrito': carrito, 'total': total})

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
        
        
