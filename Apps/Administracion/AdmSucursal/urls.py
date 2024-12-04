from django.urls import include, path

from Apps.Administracion.AdmSucursal.Views.AdmSucursalView import CrearSucursalView

# from Apps.Administracion.AdmPais.Views.AdmPaisViews import ListaPaisesView
 
urlpatterns = [
    path('crear',CrearSucursalView.as_view(),name ='Metodo para crear sucursales')
]