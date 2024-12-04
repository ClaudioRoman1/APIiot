from django.urls import include, path

from Apps.Administracion.AdmVehiculo.Views.AdmVehiculoView import CrearVehiculoView, InformacionVehiculoView, ListaVehiculoPorFlotaView


 
urlpatterns = [
    path('lista_por_flota',ListaVehiculoPorFlotaView.as_view(),name ='Metodo que lista vehiculos por flota'),
    path('crear',CrearVehiculoView.as_view(),name ='Metodo que crea vehiculos'),
    path('informacion',InformacionVehiculoView.as_view(),name ='Metodo entrega información de un vehículo'),
    
]