from django.urls import include, path

from Apps.Administracion.AdmCliente.Views.AdmClienteView import CrearClienteView

# from Apps.Administracion.AdmPais.Views.AdmPaisViews import ListaPaisesView
 
urlpatterns = [
    path('crear',CrearClienteView.as_view(),name ='Metodo para crear cliente y asignar un usuario admin al cliente')
]