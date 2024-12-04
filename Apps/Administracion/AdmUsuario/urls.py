from django.urls import include, path

from django.urls import path

from Apps.Administracion.AdmUsuario.Views.AdmUsuarioView import CrearUsuarioClienteView, EditarUsuarioView, InformacionPersonalView, SelectorClienteUsuarioView, ValidaRutView,ActivarUsuarioView, CrearUsuarioView, IniciarSesionView, DesactivarUsuarioView, ValidaEmailView, CambiarContraseñaView

urlpatterns = [
    path('inicia_sesion_usuario', IniciarSesionView.as_view(), name='Inicio de sesión'),
    path('selecciona_cliente', SelectorClienteUsuarioView.as_view() , name = 'Seleccionador perfil multicliente por id_ususario_cliente'),
    path('crea_nuevo_usuario', CrearUsuarioView.as_view(), name = 'Creación de usuarios'),
    path('editar_usuario', EditarUsuarioView.as_view(), name = 'Edicion de usuarios'),
    path('desactiva_usuario', DesactivarUsuarioView.as_view(), name='Desactiva usuario'),
    path('activa_usuario', ActivarUsuarioView.as_view(), name='Activa usuario'),
    path('valida_email_usuario',ValidaEmailView.as_view(), name='Metodo que valida que el email no exista'),
    path('valida_rut_usuario',ValidaRutView.as_view(), name='Metodo que valida que el rut no exista en los registros'),
    path('crea_usuario_cliente',CrearUsuarioClienteView.as_view(), name='Crea un usuario para un cliente en especifico'),
    path('cambiar_contrasena',CambiarContraseñaView.as_view(), name='Cambia contrasena de usuario'),
    path('informacion',InformacionPersonalView.as_view(), name='Retorna la información del usuario en sesión'),
    
    
    
    
]
