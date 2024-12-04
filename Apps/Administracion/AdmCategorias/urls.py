from django.urls import include, path

from Apps.Administracion.AdmCategorias.Views.AdmCategoriasView import CrearCategoriaView, DesactivarCategoriaView
 
urlpatterns = [
    path('crear', CrearCategoriaView.as_view(), name='Servicio sirve para crear categporia'),
    path('eliminar', DesactivarCategoriaView.as_view(), name='Servicio para eliminar categoría')
]
