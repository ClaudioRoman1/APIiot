

class MensajeRetornos():
    mensajeCreacionOk = "creacion-ok"
    mensajeBusquedaOk = "busqueda-ok"
    mensajeBusquedaOkSr = "busqueda-ok-sr"
    mensajeErrorCreacion = "creacion-fallida"
    mensajeErrorBusqueda = "busqueda-fallida"
    mensajeErrorSerializador = "Error serializador"
    mensajeNoExisteCategoria = "not-categoria"
    mensajeCategoriaEliminada = "categoria-eliminada"
    mensajeEdicionOK= "edicion-ok"
    mensajeErrorEdicionNoExisteUsuario = "edicion-error-1"
    mensajeErrorInterno = 'error-interno'
    mensajeDesactivacionOK='desactivar-ok'
    mensajePerfilYaAsignado ='perfil-ya-asignado'
    mensajeUsuarioClienteNoExiste= 'usuario-no-pertenece-cliente'
    mensajeNoEsAdmin = 'no-admin'
    mensajeCorreoExiste = 'correo-existe'
    mensajeRutExiste = 'rut-existe'
    mensajeUsuarioNoExiste='usuario-no-existe'
    mensajeUsuarioActivo = 'usuario-activo'
    mensajeClienteNoExiste='cliente-no-existe'
    mensajeErrorNoExiste ='no-existe'
    mensajeErrorExistePatente ='existe-patente'
    mensajeErrorExisteDispositivo = 'existe-dispositivo'
    mensajeErrorVehiculoYaAsignado = 'vehiculo-asignado-usuario'
class MensajeParametros():
    parametroJson= "Debe ser un json"
    parametroEntero = "Debe ser un entero"
    parametroString = "Debe ser una string"
    parametroFecha = "El formato de fecha es DD-MM-YY"
    parametroRequerido = "El parámetro es requerido"
    parametroUsuarioClienteoExiste = "usuario-cliente-no-existe"
    
class DominiosEnum(): 
    admin = 1
    user = 2
class constantesList():
    usuarioAdministrador = [1,2]
    usuarioAdminCliente = 2
    usuarioConductor=[3]
    
class estadosSolicitud():
    pendiente =1
    aceptada =0
    rechazada = 2
    cancelada = 3

class estadoDispositivo():
    abierto = True
    cerrado = False
class notificacionesEnum():
    solicitudApertura=1
    solicitudAperturaSinImagen:2
    solicitudAperturaCompletada:3
    solicitudAperturaRechazada :4
    solicitudCanceladaPorUsuario:5
    solicitudCanceladaPorAdministrador:6
    asignacionDispositivo:7
    desasignacionDispositivo:8
    dispositivoAbierto:9
    dispositivoCerrado:10
    
    
    
    
