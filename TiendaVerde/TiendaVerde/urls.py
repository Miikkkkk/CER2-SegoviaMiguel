"""
URL configuration for TiendaVerde project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tienda import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rutas de páginas públicas
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='catalogo'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('registro/', views.registro, name='registro'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Logout, redirige al inicio
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Solo usuarios autenticados
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),  # Vista de carrito solo para autenticados
]


