
from rest_framework.response import Response 
from rest_framework import status, generics
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.views import APIView
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.Administracion.AdmUsuario.Serializers.LoginSerializer import ActivarUsuarioSerializer, CrearUsuarioSerializer, DesactivarUsuarioSerializer, EditarUsuarioSerializer, ValidaEmailSerializer, ValidaRutSerializer
from Apps.Administracion.AdmUsuario.Serializers.LoginSerializer import LoginSerializer
from Apps.Administracion.AdmUsuarioClientePerfil.Models.AdmUsuarioClientePerfilModel import AdmUsuarioClientePerfil
from Apps.Administracion.AdmUsuarioClientePerfil.Serializers.AdmUsuarioClientePerfilSerializer import AsignarPerfilUsuarioSerializer, DesignarPerfilUsuarioSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import  valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction

from Funciones.Validaciones import transforma_errores_serializador, valida_perfil_admin


class AsignarPerfilUsuarioClienteView(generics.CreateAPIView):

   def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, MensajeRetornos.mensajeNoEsAdmin))
        id_usuario_cliente = request.data.get('id_usuario_cliente') 
        id_perfil = request.data.get('id_perfil')
        id_usuario_sesion =valida_jwt['usuario_id']
        fecha_proceso = datetime.now()
        
        datos = {
            'id_usuario_cliente': id_usuario_cliente,
            'id_perfil': id_perfil,
            'id_usuario_sesion': id_usuario_sesion,
            'fecha_proceso':fecha_proceso 
        }
        
        serializador = AsignarPerfilUsuarioSerializer(data = datos)

        if not serializador.is_valid():
            error_message = transforma_errores_serializador(serializador.errors)
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, error_message, 0))
        try :
            resultado = AdmUsuarioClientePerfil.crear(AdmUsuarioClientePerfil , datos)
            return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeCreacionOk, resultado, 1))
        except Exception as e : 
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 1, MensajeRetornos.mensajeErrorInterno, str(e), 0))


class DesactivarPerfilUsuarioClienteView(generics.UpdateAPIView):

    def post(self, request):
        valida_jwt = valida_token(request)
        if not valida_jwt['mensaje'] == 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'error', valida_jwt, 1))
        
        id_usuario_sesion = valida_jwt['usuario_id']
        es_admin = valida_perfil_admin(valida_jwt)
        if  not es_admin:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
        
        fecha_proceso = timezone.now()
        id_cliente_usuario_perfil = request.data.get('id_cliente_usuario_perfil')
        
        datos = {
            "id_cliente_usuario_perfil":id_cliente_usuario_perfil,
            "fecha_proceso": fecha_proceso,
            "id_usuario_sesion":id_usuario_sesion
        }
        
        serializador = DesignarPerfilUsuarioSerializer(data=datos)
        if not serializador.is_valid():
            error_message = transforma_errores_serializador(serializador.errors)
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, error_message))

        usuario_cliente_perfil = AdmUsuarioClientePerfil.objects.por_id(id_cliente_usuario_perfil).first()
        try:
            with transaction.atomic():
                AdmUsuarioClientePerfil.desactivar_perfil_cliente_usuario(usuario_cliente_perfil, datos)
                estado_consulta = status.HTTP_200_OK
                estado = 1 
                mensaje = MensajeRetornos.mensajeDesactivacionOK
        except Exception as e:
            estado_consulta = status.HTTP_500_INTERNAL_SERVER_ERROR
            estado = 0
            mensaje = 'Error: ' + str(e)
            
        return Response(retorno(status=estado_consulta, estado=estado, mensaje=mensaje))

    