
from rest_framework.response import Response 
from rest_framework import status, generics
from datetime import datetime
from Apps.Administracion.AdmPerfiles.Models.AdmPerfilesModel import AdmPerfiles
from Apps.Administracion.AdmPerfiles.Serializers.AdmPerfilesSerializer import CrearPerfilesSerializer, ListaPerfilesUsuarioClienteAdministracionSerializer
from Apps.Administracion.AdmUsuarioClientePerfil.Models.AdmUsuarioClientePerfilModel import AdmUsuarioClientePerfil
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import  valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction
from Funciones.Validaciones import transforma_errores_serializador, valida_perfil_admin


class CrearPerfilesView(generics.CreateAPIView):
   def post(self, request):
        """Crea perfiles genéricos del sistema
        Args:
          Nombre : string ,
          id_usuario_sesion : id,
          descripcion : string ,
          fecha_proceso : datetime

        Returns:
           id_perfil : int 
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario_sesion = valida_jwt['usuario_id']
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion')
        fecha_proceso = datetime.now()
        
        datos = {
            "nombre": nombre,
            "descripcion":descripcion,
            "fecha_proceso":fecha_proceso,
            "id_usuario_sesion" : id_usuario_sesion
        }
        
        serializador = CrearPerfilesSerializer(data = datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))
        
        try:
            perfil = AdmPerfiles.crear(AdmPerfiles,datos)
            resultado ={
                'id_perfil': perfil.iPerfilID
            }
            return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeCreacionOk, resultado, len(resultado)))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, MensajeRetornos.mensajeErrorInterno, str(e), 0))
            
        

    
class ListaPerfilesUsuarioClienteAdministracionView(generics.ListAPIView):
    """Lista perfiles de un usuario que pertenece a un cliente solamente si el usuario es administrador del cliente

    Args:
        generics (_type_): _description_
    """
    def post(self, request):
        valida_jwt = valida_token(request)
        if not valida_jwt['mensaje'] == 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'error', valida_jwt, 1))
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin :
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, MensajeRetornos.mensajeNoEsAdmin, 0))
        
        id_usuario_sesion = valida_jwt['usuario_id']
        id_usuario_cliente = request.data.get('id_usuario_cliente')
        id_usuario = request.data.get('id_usuario')
        
        datos = {
            "id_usuario_sesion":id_usuario_sesion,
            "id_usuario_cliente":id_usuario_cliente,
            "id_usuario":id_usuario
        }
        serializador = ListaPerfilesUsuarioClienteAdministracionSerializer(data=datos)
        if not serializador.is_valid():
            mensaje = transforma_errores_serializador(serializador.errors)
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,mensaje,0 ))

        # usuario = AdmUsuario.objects.por_id(id_usuario_activar).first()
        
        try:   
            perfiles = AdmUsuarioClientePerfil.objects.por_usuario_cliente_anotate(id_usuario_cliente)
            return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeBusquedaOk,perfiles , len(perfiles)))
            
        
        except Exception as e:
      
            
            return Response(retorno(status=status.HTTP_500_INTERNAL_SERVER_ERROR, estado=0, mensaje=MensajeRetornos.mensajeErrorInterno + str(e)))
    
