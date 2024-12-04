from django.urls import  path

from Apps.Administracion.AdmVehiculoDispositivo.Views.AdmVehiculoDispositivoView import AsignarDispositivoView, ListaDispositivosAsignadosPorVehiculosView, ListaVehiculoDispositivosPorClienteView


 
urlpatterns = [
    path('lista_por_cliente', ListaVehiculoDispositivosPorClienteView.as_view(),name ='Metodo que lista dispositivos por cliente'),
    path('lista_por_vehiculo', ListaDispositivosAsignadosPorVehiculosView.as_view(),name ='Metodo que lista dispositivos asignado a un vehiculo'),
    path('asignar',AsignarDispositivoView.as_view(),name ='Metodo que asigna dispositivo a un vehiculo'),
    
]