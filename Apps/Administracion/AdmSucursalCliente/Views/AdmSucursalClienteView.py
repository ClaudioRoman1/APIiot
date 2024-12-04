from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime
from django.db import transaction
from Apps.Administracion.AdmSucursal.Models.AdmSucursalModel import AdmSucursal
from Apps.Administracion.AdmSucursalCliente.Models.AdmSucursalClienteModel import AdmSucursalCliente
from Apps.Administracion.AdmSucursalCliente.Serializers.AdmSucursalClienteSerializer import ListaSucursalesPorClienteSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
class ListaSucursalesPorClienteView(generics.ListAPIView):
    """Servicio para agregar una sucursal a un cliente

    Args:
        id_cliente: int
    Remarks: Claudio Román 13-08-2023
    """

    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'token ' + valida_jwt['mensaje']))
        
        id_cliente = request.data.get('id_cliente')
        id_usuario = request.data.get('id_usuario') if 'id_usuario' in request.data else  valida_jwt['usuario_id']
        
        
        
        datos = {
            'id_cliente': id_cliente,
            'id_usuario': id_usuario,
        }
        
        serializador = ListaSucursalesPorClienteSerializer(data=datos)
        
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors))
        try:
            with transaction.atomic():
                sucursal_cliente = AdmSucursalCliente.objects.por_id_cliente (iclienteid=id_cliente)
                return Response(retorno(status.HTTP_200_OK, 0, MensajeRetornos.mensajeCreacionOk, sucursal_cliente, len(sucursal_cliente)))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,str(e) ))
        