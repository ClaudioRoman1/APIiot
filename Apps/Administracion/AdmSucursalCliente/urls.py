from django.urls import include, path

from Apps.Administracion.AdmSucursalCliente.Views.AdmSucursalClienteView import ListaSucursalesPorClienteView

# from Apps.Administracion.AdmPais.Views.AdmPaisViews import ListaPaisesView
 
urlpatterns = [
    path('listar_por_clientes',ListaSucursalesPorClienteView.as_view(),name ='Metodo que lista sucursales por cliente')
    
]