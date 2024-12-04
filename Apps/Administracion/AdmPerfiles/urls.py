
from django.urls import path

from Apps.Administracion.AdmPerfiles.Views.AdmPerfilesView import CrearPerfilesView, ListaPerfilesUsuarioClienteAdministracionView

urlpatterns = [
    path('crear', CrearPerfilesView.as_view(), name = 'Creación de perfiles'),
    path('administracion/usuariocliente/listar', ListaPerfilesUsuarioClienteAdministracionView.as_view(), name = 'Listados de perfiles de un usuario cliente para el perfil solo de administrador'),
]
