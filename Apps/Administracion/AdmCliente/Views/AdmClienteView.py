from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmCliente.Serializers.AdmClienteSerializer import CrearClienteSerializer
from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction


class CrearClienteView (generics.CreateAPIView):
    # Funcion para crear cliente
    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_usuario_creacion = valida_jwt['usuario_id']
        razon_social = request.data.get('razon_social')
        nombre_fantasia = request.data.get('nombre_fantasia')
        identificador = request.data.get('identificador')
        id_usuario = request.data.get('id_usuario')
        fecha_proceso = timezone.now()

        datos = {
            "id_usuario": id_usuario,
            "razon_social": razon_social,
            "identificador": identificador,
            "nombre_fantasia": nombre_fantasia,
            "fecha_proceso": fecha_proceso,
            "id_usuario_sesion": id_usuario_creacion
        }

        serializador = CrearClienteSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

        try:
            with transaction.atomic():
                cliente = AdmCliente.crear(self, datos)
                usuario = AdmUsuario.objects.por_id(
                    datos['id_usuario']).first()

                AdmClienteUsuario.crear_cliente_usuario(
                    AdmClienteUsuario, datos, usuario, cliente)
            return Response(retorno(status.HTTP_201_CREATED, 1, MensajeRetornos.mensajeCreacionOk))
        except Exception as a:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))