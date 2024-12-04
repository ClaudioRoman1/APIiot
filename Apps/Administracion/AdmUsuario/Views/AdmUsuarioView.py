
from rest_framework.response import Response 
from rest_framework import status, generics
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.views import APIView
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.Administracion.AdmUsuario.Serializers.LoginSerializer import ActivarUsuarioSerializer, CambiarContrasenaSerializer, CrearUsuarioClienteSerializer, CrearUsuarioSerializer, DesactivarUsuarioSerializer, EditarUsuarioSerializer, InformacionPersonalSerializer, SelectorClienteUsuarioSerializer, ValidaEmailSerializer, ValidaRutSerializer
from Apps.Administracion.AdmUsuario.Serializers.LoginSerializer import LoginSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import crea_token_jwt, valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from Funciones.Validaciones import transforma_errores_serializador, valida_perfil_admin


class IniciarSesionView(APIView):
   def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = LoginSerializer(data={'email': email , 'password': password })
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Realizar la autenticación del usuario con el modelo personalizado de usuario
        usuario = AdmUsuario.objects.por_correo(email).first()
        if not usuario:
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'Credenciales inválidas'))

        is_match = check_password(password,usuario.vcContrasena)
        if  not is_match :
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'Credenciales inválidas'))
        
          # Obtén el usuario por su clave primaria

# Obtén el objeto AdmClienteUsuario relacionado con el usuario
        id_cliente_usuario = AdmClienteUsuario.objects.obtiene_cliente_usuario(usuario.iUsuarioID)
        id_clientes = AdmClienteUsuario.objects.clientes_por_id_usuario(usuario.iUsuarioID)
        payload = {
            'usuario_id': usuario.iUsuarioID,
            'id_cliente': id_clientes,
            'id_cliente_usuario':id_cliente_usuario,
            'exp': datetime.utcnow() + timedelta(weeks=3)  # Configurar la expiración del token
        }
        
        token = crea_token_jwt(payload)
        resultado = {
            'access_token':token,
            'refresh_token': token
        }
        
        return Response(retorno(status.HTTP_200_OK, 1, 'Inicio Exitoso', resultado, 1))


class SelectorClienteUsuarioView(APIView):
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario = valida_jwt['usuario_id']
        id_usuario_cliente = request.data.get('id_usuario_cliente')
        datos= {
            "id_usuario" : id_usuario,
            "id_usuario_cliente": id_usuario_cliente
        }
      
        serializador = SelectorClienteUsuarioSerializer(data = datos)
        if not serializador.is_valid():
            error_message = transforma_errores_serializador(serializador.errors)
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, error_message, 0))
            
        
        try:
            payload = {
            'usuario_id': id_usuario,
            'id_cliente': 1,
            'id_usuario_cliente':id_usuario_cliente,
            # 'exp': datetime.utcnow() + timedelta(hours=1)  # Configurar la expiración del token
            }
        
            token = crea_token_jwt(payload)
            resultado = {
                'access_token':token,
                'refresh_token': token
            }
            
            return Response(retorno(status.HTTP_200_OK, 1, 'Inicio Exitoso', resultado, 1))

        except Exception as a:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))


    

    
class CrearUsuarioView (generics.CreateAPIView):
    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario_sesion = valida_jwt['usuario_id']
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
        nombre = request.data.get('nombres')
        apellidos = request.data.get('apellidos')
        identificador = request.data.get('identificador')
        num_cel = request.data.get('num_cel')
        correo_electronico = request.data.get('correo_electronico')
        id_pais = request.data.get('id_pais')
        direccion = request.data.get('direccion')
        contraseña = request.data.get('contrasena')
        id_rol = request.data.get('id_rol')
        fecha_proceso = timezone.now()
        hashed_password = make_password(contraseña)
    
        existe_por_correo = AdmUsuario.objects.por_correo(correo_electronico).first()
        existe_por_rut = AdmUsuario.objects.por_rut(identificador).first()
        if existe_por_correo:
                return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, 'correo-registrado'))
        if existe_por_rut:
                return Response(retorno(status.HTTP_200_OK, 0, 'rut-registrado'))
            
        datos = {
        "nombre":nombre,
        "apellidos":apellidos,
        "identificador":identificador,
        "num_cel":num_cel,
        "correo_electronico":correo_electronico,
        "id_pais":id_pais,
        "direccion":direccion,
        "contraseña":hashed_password,
        "id_rol":id_rol,
        "id_usuario_sesion":id_usuario_sesion,
        "fecha_proceso": fecha_proceso 
        }
        
        serializador = CrearUsuarioSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

        with transaction.atomic():
            try:
                AdmUsuario.crear(self,datos)
                return Response(retorno(status.HTTP_201_CREATED, 1, 'Creación exitosa'))
            except Exception as a:
                return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))
    
            
class DesactivarUsuarioView(generics.UpdateAPIView):

    def post(self, request):
        valida_jwt = valida_token(request)
        if not valida_jwt['mensaje'] == 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'error', valida_jwt, 1))
        
        id_usuario = valida_jwt['usuario_id']
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
        
        fecha_proceso = timezone.now()
        id_usuario_desactivar = request.data.get('id_usuario_desactivar')
        
        datos = {
            "id_usuario":id_usuario,
            "id_usuario_desactivar":id_usuario_desactivar,
            "fecha_proceso": fecha_proceso
        }
        
        serializador = DesactivarUsuarioSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors))

        usuario = AdmUsuario.objects.por_id(id_usuario_desactivar).first()
        try:
            with transaction.atomic():
                AdmUsuario.eliminacion_logica_usuario(usuario, datos)
                estado_consulta = status.HTTP_200_OK
                estado = 1 
                mensaje = 'Desactivado con éxito'
        except Exception as e:
            estado_consulta = status.HTTP_500_INTERNAL_SERVER_ERROR
            estado = 0
            mensaje = 'Error: ' + str(e)
            
        return Response(retorno(status=estado_consulta, estado=estado, mensaje=mensaje))

    
class ActivarUsuarioView(generics.UpdateAPIView):

    def post(self, request):
        valida_jwt = valida_token(request)
        if not valida_jwt['mensaje'] == 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'error', valida_jwt, 1))
        
        id_usuario = valida_jwt['usuario_id']
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'No tiene permisos de administrador'))
        
        fecha_proceso = timezone.now()
        id_usuario_activar = request.data.get('id_usuario_activar')
        
        datos = {
            "id_usuario":id_usuario,
            "id_usuario_activar":id_usuario_activar,
            "fecha_proceso": fecha_proceso
        }
        serializador = ActivarUsuarioSerializer(data=datos)
        if not serializador.is_valid():
            mensaje = transforma_errores_serializador(serializador.errors)
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, mensaje,0))
    
        try:
            with transaction.atomic():
                usuario = AdmUsuario.objects.por_id(id_usuario_activar).first()
                AdmUsuario.activar_usuario(usuario, datos)
                estado_consulta = status.HTTP_200_OK
                estado = 1 
                mensaje = 'Usuario activado con éxito'
        except Exception as e:
            estado_consulta = status.HTTP_500_INTERNAL_SERVER_ERROR
            estado = 0
            mensaje = 'Error: ' + str(e)
            
        return Response(retorno(status=estado_consulta, estado=estado, mensaje=mensaje))
    

class ValidaEmailView(generics.GenericAPIView):

    def post(self, request):
        correo_electronico = request.data.get('correo_electronico')
        datos = {}
        datos['correo_electronico'] = correo_electronico
        serializador = ValidaEmailSerializer(data=datos)
        
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))
        existe_por_correo = AdmUsuario.objects.por_correo(correo_electronico).first()
        if existe_por_correo:
                return Response(retorno(status.HTTP_200_OK, 1, 'correo-invalido'))
        
        return Response(retorno(status.HTTP_200_OK, 1, 'correo-valido'))
 
 
class ValidaRutView(generics.GenericAPIView):

    def post(self, request):
        identificador = request.data.get('identificador')
        datos = {}
        datos['identificador'] = identificador
        serializador = ValidaRutSerializer(data=datos)
        
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors,))
    
        existe_por_rut = AdmUsuario.objects.por_rut(identificador).first()
       
        if existe_por_rut:
                return Response(retorno(status.HTTP_200_OK, 1, 'rut-invalido'))
        
        return Response(retorno(status.HTTP_200_OK, 1, 'rut-valido'))

class EditarUsuarioView(APIView):
    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        
        id_usuario_sesion = valida_jwt['usuario_id']
        id_usuario = valida_jwt['usuario_id']
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        num_cel = request.data.get('num_cel')
        correo_electronico = request.data.get('correo_electronico')
        id_pais = request.data.get('id_pais')
        contrasena = request.data.get('contrasena')
        direccion = request.data.get('direccion')
        fecha_proceso = timezone.now()

        existe_por_correo = AdmUsuario.objects.por_correo(correo_electronico).first()
        datos = {}

        if not existe_por_correo:
            datos["correo_electronico"] = correo_electronico

        datos.update({
            "id_usuario": id_usuario,
            "nombre":nombre,
            "apellidos":apellidos,
            "num_cel":num_cel,
            "correo_electronico":correo_electronico,
            "id_pais":id_pais,
            "direccion":direccion,
            "id_usuario_sesion":id_usuario_sesion,
            "fecha_proceso": fecha_proceso 
        })

        serializador = EditarUsuarioSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

        usuario = AdmUsuario.objects.por_id(usuarioid=id_usuario).first()
        if usuario is None:
            return Response (retorno(status.HTTP_404_NOT_FOUND , 0 , MensajeRetornos.mensajeErrorEdicionNoExisteUsuario))
            
        if usuario.iUsuarioID != id_usuario_sesion:
            es_admin = valida_perfil_admin(valida_jwt)
            if not es_admin:
                return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))

        is_match = check_password(contrasena, usuario.vcContrasena)
        if not is_match:
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'Credenciales inválidas'))

        with transaction.atomic():
            try:
                # Mapeo de nombres de campos
                mapeo_campos = {
                    'nombre': 'vcNombre',
                    'apellidos': 'vcApellidos',
                    'num_cel': 'vcNumeroMovil',
                    'correo_electronico': 'vcCorreoElectronico',
                    'direccion': 'vcDireccion',
                    'id_pais': 'iPaisID_id',
                    'contrasena': 'vcContrasena',
                    "id_usuario_sesion": "iUsuarioUltimaModificacionID",
                    "fecha_proceso": "dtmUltimaModificacion"
                }

                # Mapea los nombres de campos en datos a los nombres de campos a verificar
                datos_mapeados = {mapeo_campos[nombre]: datos[nombre] for nombre in datos if nombre in mapeo_campos}

     
                respuesta = AdmUsuario.editar(AdmUsuario, datos_mapeados, id_usuario)
                mensaje = MensajeRetornos.mensajeEdicionOK
                status_retorno = status.HTTP_200_OK
                estado=1
                if respuesta == None :
                    mensaje= MensajeRetornos.mensajeErrorInterno
                    status_retorno = status.HTTP_500_INTERNAL_SERVER_ERROR
                    estado=0
                    
                elif respuesta == 'error-1':
                    mensaje = MensajeRetornos.mensajeErrorEdicionNoExisteUsuario
                    status_retorno = status.HTTP_404_NOT_FOUND 
                    estado=0
                usuario = InformacionPersonalSerializer.to_representation(self,usuario)
                    
                return Response(retorno(status_retorno, estado, mensaje,usuario))
            except Exception as a:
                return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'ERROR: ' + str(a)))



class CrearUsuarioClienteView (generics.CreateAPIView):
    
    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario_sesion = valida_jwt['usuario_id']
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
        id_usuario_sesion = valida_jwt['usuario_id']
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        num_cel = request.data.get('num_cel')
        correo_electronico = request.data.get('correo_electronico')
        id_pais = request.data.get('id_pais')
        contrasena = request.data.get('contrasena')
        direccion = request.data.get('direccion')
        identificador = request.data.get('identificador')
        
        correo_electronico = request.data.get('correo_electronico')
        id_pais = request.data.get('id_pais')
        id_cliente = request.data.get('id_cliente')
        fecha_proceso = timezone.now()
        hashed_password = make_password(contrasena)
    
       
            
        datos = {
        "nombre":nombre,
        "apellidos":apellidos,
        "identificador":identificador,
        "num_cel":num_cel,
        "correo_electronico":correo_electronico,
        "id_pais":id_pais,
        "direccion":direccion,
        "contrasena":hashed_password,
        "id_usuario_sesion":id_usuario_sesion,
        "fecha_proceso": fecha_proceso ,
        "id_cliente" : id_cliente
        }
        
        serializador = CrearUsuarioClienteSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

        try:
            with transaction.atomic():
                usuario = AdmUsuario.crear(self,datos)
                cliente = AdmCliente.objects.por_id(id_cliente).activo().first()
                cliente_usuario = AdmClienteUsuario.crear_cliente_usuario(self,datos,usuario , cliente )
                return Response(retorno(status.HTTP_201_CREATED, 1, 'Creación exitosa'))
        except Exception as a:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))
        
class CambiarContraseñaView(APIView):
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario = request.data.get('id_usuario')
        antigua_contrasena = request.data.get('antigua_contrasena')
        nueva_contrasena = request.data.get('nueva_contrasena')
        
        datos={
            'id_usuario' : id_usuario,
            'nueva_contrasena':nueva_contrasena,
            'antigua_contrasena':antigua_contrasena
        }
        usuario = AdmUsuario.objects.por_id(id_usuario).first()
        serializador = CambiarContrasenaSerializer(data=datos, context ={'usuario': usuario})
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

        try:
            datos['nueva_contrasena']= make_password(nueva_contrasena)
            datos['fecha_proceso'] = timezone.now()
            with transaction.atomic():
                usuario = AdmUsuario.cambiar_contrasena(self,usuario,datos)
                return Response(retorno(status.HTTP_200_OK, 1, 'Cambio de contrasena exitoso'))
        except Exception as a:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 1, 'ERROR: ' + str(a)))
        
        
class InformacionPersonalView(APIView):
    def get(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario_sesion = valida_jwt['usuario_id']
        try:
            usuario  = AdmUsuario.objects.por_id(id_usuario_sesion).activo().first()
            if (usuario):
                informacion = InformacionPersonalSerializer.to_representation(self,usuario)
                return Response(retorno(status.HTTP_200_OK, 1, 'Usuario encontrado', informacion))
            else :
                return Response(retorno(status.HTTP_200_OK, 0, 'Usuario no encontrado'))
            
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 1, 'ERROR: ' + str(e)))
            
        
