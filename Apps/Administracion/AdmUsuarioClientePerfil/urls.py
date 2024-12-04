
from django.urls import path
from Apps.Administracion.AdmUsuarioClientePerfil.Views.AdmUsuarioClientePerfilView import AsignarPerfilUsuarioClienteView, DesactivarPerfilUsuarioClienteView

urlpatterns = [
    path('asignar', AsignarPerfilUsuarioClienteView.as_view(), name = 'Asigna perfil  a un usuario que pertenece a un cliente'),
    path('desasignar', DesactivarPerfilUsuarioClienteView.as_view(), name='Desactiva perfil a un usuario que pertenece a un cliente'),
    # path('inicia_sesion_usuario', IniciarSesionView.as_view(), name='Inicio de sesión'),
    # path('editar_usuario', EditarUsuarioView.as_view(), name = 'Edicion de usuarios'),
    # path('activa_usuario', ActivarUsuarioView.as_view(), name='Activa usuario'),
    # path('valida_email_usuario',ValidaEmailView.as_view(), name='Metodo que valida que el email no exista'),
    # path('valida_rut_usuario',ValidaRutView.as_view(), name='Metodo que valida que el rut no exista en los registros')
    
    
    
]
