from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime
from django.db import transaction
from Apps.Administracion.AdmSucursal.Models.AdmSucursalModel import AdmSucursal
from Apps.Administracion.AdmSucursalCliente.Models.AdmSucursalClienteModel import AdmSucursalCliente
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
class CrearSucursalView(generics.CreateAPIView):
    """Servicio para agregar una sucursal a un cliente

    Args:
        id_cliente: int
        nombre_sucursal : string
        id_pais : int
        id_region : int
        id_comuna : int
    Remarks: Claudio Román 13-08-2023
    """

    def post(self, request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, 'token ' + valida_jwt['mensaje']))
    
        id_cliente = request.data.get('id_cliente')
        id_pais = request.data.get('id_pais')
        id_region = request.data.get('id_region')
        id_comuna = request.data.get('id_comuna')
        calle = request.data.get('calle')
        nombre_sucursal = request.data.get('nombre_sucursal')
        fecha_proceso = datetime.now()
        id_usuario_sesion = valida_jwt['usuario_id']
        
        datos = {
            'id_cliente': id_cliente,
            'id_pais': id_pais,
            'id_region': id_region,
            'id_comuna': id_comuna,
            'calle': calle,
            'nombre_sucursal': nombre_sucursal,
            'fecha_proceso': fecha_proceso,
            'id_usuario_sesion': id_usuario_sesion,
        }
        
        # serializador = AgregarSucursalClienteSerializer(data=datos)
        
        # if not serializador.is_valid():
        #     return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors))
        try:
            with transaction.atomic():
                sucursal = AdmSucursal.crear_sucursal(AdmSucursal, datos)
                sucursal_cliente = AdmSucursalCliente.crear_sucursal_cliente (AdmSucursalCliente , datos,sucursal)
                resultado = {
                    "id_sucursal":sucursal.SucursalID,
                    "id_sucursal_cliente": sucursal_cliente.iSucursalClienteID
                }
                return Response(retorno(status.HTTP_200_OK, 0, MensajeRetornos.mensajeCreacionOk, resultado, 1))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,str(e) ))
        
        