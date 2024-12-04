from django.urls import include, path

from Apps.Administracion.AdmSolicitud.Views.AdmSolicitudView import CancelarSolicitudView, ListadoVehiculosConSolicitudesView, SolicitudAbrirDispositivoView, InformacionSolicitudView




 
urlpatterns = [
    # path('lista_por_flota',ListaVehiculoPorFlotaView.as_view(),name ='Metodo que lista vehiculos por flota'),
    path('abrir',SolicitudAbrirDispositivoView.as_view(),name ='Metodo que crea vehiculos'),
    path('informacion',InformacionSolicitudView.as_view(),name ='Metodo envía información del dispositivo'),
    path('cancelar',CancelarSolicitudView.as_view(),name ='Metodo para cancelar las solicitudes'),
    path('administrador/vehiculosconsolicitud',ListadoVehiculosConSolicitudesView.as_view(),name ='Metodo para cancelar las solicitudes'),
    
    
    # path('informacion',InformacionVehiculoView.as_view(),name ='Metodo entrega información de un vehículo'),
    
]