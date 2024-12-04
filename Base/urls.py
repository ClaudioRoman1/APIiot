"""
URL configuration base for sisSolped project.

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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paises/', include('Apps.Administracion.AdmPais.urls')),
    path('regiones/', include('Apps.Administracion.AdmRegion.urls')),
    path('usuarios/', include('Apps.Administracion.AdmUsuario.urls')),
    path('categorias/', include('Apps.Administracion.AdmCategorias.urls')),
    path('clientes/', include('Apps.Administracion.AdmCliente.urls')),
    path('sucursales/',include('Apps.Administracion.AdmSucursal.urls')),
    path('sucursalcliente/',include('Apps.Administracion.AdmSucursalCliente.urls')),
    path('perfiles/',include('Apps.Administracion.AdmPerfiles.urls')),
    path('usuarioclienteperfil/',include('Apps.Administracion.AdmUsuarioClientePerfil.urls')),
    path('flotas/',include('Apps.Administracion.AdmFlota.urls')),
    path('vehiculos/',include('Apps.Administracion.AdmVehiculo.urls')),
    path('vehiculodispositivo/' , include('Apps.Administracion.AdmVehiculoDispositivo.urls')),
    path('dispositivos/' , include('Apps.Administracion.AdmDispositivo.urls')),
    path('usuariovehiculos/' , include('Apps.Administracion.AdmUsuarioVehiculo.urls')),
    path('solicitudes/' , include('Apps.Administracion.AdmSolicitud.urls')),
    path('test/' , include('Apps.Administracion.AdmTest.urls')),
    
    
    
    
    
    
    # path('paises/',include('Apps.Administracion.AdmPais.urls'))
    
]
