from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.Administracion.AdmVehiculo.Serializers.AdmVehiculoSerializer import CrearVehiculoSerializer, InformacionVehiculoSerializer, ListaVehiculoPorFlotaSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction

class  ListaVehiculoPorFlotaView(generics.ListAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_flota = request.data.get('id_flota')
        datos = {
            'id_flota':id_flota
        }
        serializer = ListaVehiculoPorFlotaSerializer(data=datos)
        if serializer.is_valid():
            vehiculos = AdmVehiculo.objects.por_flota(iflotaid = id_flota).activo()
            ls_vehiculos = list(vehiculos)
            
            if len(ls_vehiculos) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay vehiculos para esta flota', None,None))
        
            lista_vehiculos = ListaVehiculoPorFlotaSerializer(vehiculos,many=True)
            lista_vehiculos_serializadas= lista_vehiculos.data 
            total_reg = len(lista_vehiculos_serializadas)
        
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_vehiculos_serializadas, total_reg ))


class CrearVehiculoView(generics.CreateAPIView):
    """Metodo para crear un vehiculo en una flota

    Args:
        id_flota (int): id de la flota que pertenece a un cliente
        num_patente (string) : Patente del vehículo
        marca (string) : marca del vehiculo
        cantidad_litros (decimal - float) : litros que puede almacenar el camión
        ano (int) : año del vehículo
    """
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario_sesion = valida_jwt['usuario_id']
        id_flota = request.data.get('id_flota')
        num_patente = request.data.get('num_patente')
        marca = request.data.get('marca')
        ano = request.data.get('ano')
        cantidad_litros = request.data.get('cantidad_litros')
        
        fecha_proceso = datetime.now()
        
        datos = {
            "id_flota": id_flota,
            "num_patente": num_patente,
            "marca":marca,
            "ano":ano,
            "cantidad_litros":cantidad_litros,
            "id_usuario_sesion" : id_usuario_sesion,
            "fecha_proceso": fecha_proceso
        }
        
        serializador = CrearVehiculoSerializer(data = datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))
        
        try:
            with transaction.atomic():
                datos['num_patente']= num_patente.upper()
                vehiculo = AdmVehiculo.crear(AdmVehiculo,datos)
                return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeCreacionOk,{"id_vehiculo": vehiculo.iVehiculoID} ))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, MensajeRetornos.mensajeErrorInterno, str(e), 0))
            
        

class InformacionVehiculoView(generics.GenericAPIView):
    """Metodo para obtener la información de un vehiculo y dispositivo
    Retorno: retorno
    Elaborado por: CRoman 15-11-24
       """
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        id_vehiculo = request.data.get('id_vehiculo')
        datos = {
            'id_vehiculo':id_vehiculo
        }
        serializer = InformacionVehiculoSerializer(data=datos)
        if serializer.is_valid():
            vehiculo = AdmVehiculo.objects.por_id(ivehiculoid = id_vehiculo).activo().first()
            
            
            if not vehiculo :
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay dispositivos ', None,None))
            try:
                lista_dispositivos = InformacionVehiculoSerializer(instance=vehiculo)
                lista_dispositivos_serializadas= lista_dispositivos.data 
                total_reg = len(lista_dispositivos_serializadas)
                return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_dispositivos_serializadas, total_reg ))
            except Exception as e:
                return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0,  'Error: ' +  str(e)))
                
        else:
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,  serializer.errors))