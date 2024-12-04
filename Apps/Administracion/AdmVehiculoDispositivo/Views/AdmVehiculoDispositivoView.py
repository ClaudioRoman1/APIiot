from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmVehiculoDispositivo.Models.AdmVehiculoDispositivoModel import AdmVehiculoDispositivo
from Apps.Administracion.AdmVehiculoDispositivo.Serializers.AdmVehiculoDispositivoSerializer import AsignarDispositivoSerializer, ListaDispositivosAsignadosPorVehiculosSerializer, ListaVehiculoDispositivosSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction

class  AsignarDispositivoView(generics.CreateAPIView):
    """Metodo que sirve para asignar un dispositivo a un vehiculo el vehiculo debe estar activo al igual que el dispositivo
        params:
        id_dispositivo (int)
        id_vehiculo (int)
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_vehiculo = request.data.get('id_vehiculo')
        id_dispositivo = request.data.get('id_dispositivo')
        datos = {
            'id_vehiculo':id_vehiculo,
            'id_dispositivo':id_dispositivo
        }
        serializador = AsignarDispositivoSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,  serializador.errors))
        
        try:
            with transaction.atomic():
                datos['fecha_proceso'] = datetime.now()
                datos['id_usuario_sesion'] = valida_jwt['usuario_id']
                asignacion = AdmVehiculoDispositivo.crear(AdmVehiculoDispositivo, datos)
                return Response(retorno(status.HTTP_200_OK, 1,  MensajeRetornos.mensajeCreacionOk))

        except Exception as e :
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,  str(e)))

        
class  ListaVehiculoDispositivosPorClienteView(generics.ListAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
       """
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_cliente = request.data.get('id_cliente')
        datos = {
            'id_cliente':id_cliente
        }
        serializer = ListaVehiculoDispositivosSerializer(data=datos)
        if serializer.is_valid():
            dispositivos = AdmVehiculoDispositivo.objects.por_cliente(iclienteid = id_cliente).activo()
            ls_dispositivos = list(dispositivos)
            
            if len(ls_dispositivos) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay dispositivos ', None,None))
            try:
                lista_dispositivos = ListaVehiculoDispositivosSerializer(instance=dispositivos,many=True)
                lista_dispositivos_serializadas= lista_dispositivos.data 
                total_reg = len(lista_dispositivos_serializadas)
                return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_dispositivos_serializadas, total_reg ))
            except Exception as e:
                return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,  'Error: ' +  str(e)))

                
        else:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,  serializer.errors))
        

class  ListaDispositivosAsignadosPorVehiculosView(generics.ListAPIView):
    """Metodo que lista los dispositivos asociados a un vehíclo
       Retorno: retorno
       Elaborado por: CRoman 13-11-24
       """
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_vehiculo = request.data.get('id_vehiculo')
        datos = {
            'id_vehiculo':id_vehiculo
        }
        serializer = ListaDispositivosAsignadosPorVehiculosSerializer(data=datos)
        if serializer.is_valid():
            dispositivos = AdmVehiculoDispositivo.objects.por_vehiculo(ivehiculoid = id_vehiculo).activo()
            ls_dispositivos = list(dispositivos)
            
            if len(ls_dispositivos) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay dispositivos ', None,None))
            try:
                lista_dispositivos = ListaDispositivosAsignadosPorVehiculosSerializer(instance=dispositivos,many=True)
                lista_dispositivos_serializadas= lista_dispositivos.data 
                total_reg = len(lista_dispositivos_serializadas)
                return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_dispositivos_serializadas, total_reg ))
            except Exception as e:
                return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,  'Error: ' +  str(e)))

                
        else:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,  serializer.errors))


