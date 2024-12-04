from django.urls import include, path

from Apps.Administracion.AdmUsuarioVehiculo.Views.AdmUsuarioVehiculoView import AsignarVehiculoUsuarioView, BusquedaVehiculosPorUsuarioConceptoView, ListaVehiculosAsignadosUsuarioView, ListaVehiculosAsignadosView


 
urlpatterns = [
    path('lista_por_cliente',ListaVehiculosAsignadosView.as_view(),name ='Metodo que lista dispositivos asignados de un cliente'),
    path('lista_por_usuario',ListaVehiculosAsignadosUsuarioView.as_view(),name ='Metodo que lista vehiculos asignados a un usuario'),
    path('asignar_a_usuario', AsignarVehiculoUsuarioView.as_view(), name='Metodo que asigna vehiculos a usuarios'),
    path('busqueda_concepto', BusquedaVehiculosPorUsuarioConceptoView.as_view(),name= 'Método que busca vehiculos por flota o patente')
]