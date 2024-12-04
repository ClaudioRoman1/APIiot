from ast import Try
from datetime import datetime
from json import JSONEncoder
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmSolicitud.Models.AdmSolicitudModel import AdmSolicitud
from Apps.Administracion.AdmSolicitud.Serializers.AdmSolicitudSerializer import CancelarSolicitudSerializer, ListadoVehiculosConSolicitudesSerializer, SolicitudAbrirDispositivoSerializer, InformacionSolicitudSerializer
from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.Administracion.AdmUsuarioVehiculo.Views import AdmUsuarioVehiculoView
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.Administracion.AdmVehiculo.Serializers.AdmVehiculoSerializer import CrearVehiculoSerializer, InformacionVehiculoSerializer, ListaVehiculoPorFlotaSerializer
from Apps.Administracion.AdmVehiculoDispositivo.Models.AdmVehiculoDispositivoModel import AdmVehiculoDispositivo
from Apps.RestBase.Constantes import MensajeRetornos, estadosSolicitud
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction

from Funciones.Validaciones import valida_perfil_admin

class  SolicitudAbrirDispositivoView(generics.CreateAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario = request.data.get('id_usuario')
        id_dispositivo = request.data.get('id_dispositivo')
        id_vehiculo = request.data.get('id_vehiculo')
        imagenes = request.data.get('imagenes')
        id_usuario_sesion = valida_jwt['usuario_id']
        
        datos = {
            'id_usuario':id_usuario,
            'id_dispositivo':id_dispositivo,
            'id_vehiculo':id_vehiculo,
            'imagenes' : imagenes,
            'id_usuario_sesion':id_usuario_sesion
        }
        serializer = SolicitudAbrirDispositivoSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, serializer.errors))
        try : 
            with transaction.atomic():
                id_usuario_vehiculo = AdmUsuarioVehiculo.objects.por_usuario_por_vehiculo_simple( id_usuario,id_vehiculo).activo().first()
                if not id_usuario:
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'El usuario no tiene el vehículo asignado'))
                    
                id_vehiculo_dispositivo = AdmVehiculoDispositivo.objects.por_vehiculo_por_dispositivo(id_vehiculo,id_dispositivo).activo().first()
                if not id_vehiculo_dispositivo:
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'El vehiculo no tiene el dispositivo asignado'))
                
                solicitud = AdmSolicitud.objects.por_usuariovehiculo_por_vehiculodispositivo_pendiente(id_usuario_vehiculo, id_vehiculo_dispositivo)
                
                if solicitud.exists():
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'Ya hay una solicitud en curso',solicitud.values()))
                    
                datos['id_usuario_vehiculo']= id_usuario_vehiculo
                datos['id_vehiculo_dispositivo']= id_vehiculo_dispositivo

                datos['fecha_proceso'] = datetime.now()
                
                solicitd = AdmSolicitud.crear(AdmSolicitud,datos)
                return Response(retorno(status.HTTP_200_OK, 1, 'Solicitud creada con éxito'))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al reralizar la solicitud: ' + str(e)  ))
        

class InformacionSolicitudView(generics.ListAPIView):
    def post(self, request):
        """Servicio que entrega la información de las solicitudes realizadas por un usuario

        Args:
            id_usuario: int
            id_dispositivo: int
            id_vehiculo: int

        Returns:
            _type_: _description_
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario = request.data.get('id_usuario')
        id_dispositivo = request.data.get('id_dispositivo')
        id_vehiculo = request.data.get('id_vehiculo')
        id_usuario_sesion = valida_jwt['usuario_id']
        
        datos = {
            'id_usuario':id_usuario,
            'id_dispositivo':id_dispositivo,
            'id_vehiculo':id_vehiculo,
            'id_usuario_sesion':id_usuario_sesion
        }
        serializer = InformacionSolicitudSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, serializer.errors))
        try : 
            id_usuario_vehiculo = AdmUsuarioVehiculo.objects.por_usuario_por_vehiculo_simple( id_usuario,id_vehiculo).first()
            if not id_usuario_vehiculo:
                return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'Nunca ha sido asignado este vehículo al usuario'))
                
            id_vehiculo_dispositivo = AdmVehiculoDispositivo.objects.por_vehiculo_por_dispositivo(id_vehiculo,id_dispositivo).first()
            if not id_vehiculo_dispositivo:
                return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'Nunca ha sido asignado el dispositivo al vehículo'))
            
            datos['id_usuario_vehiculo']= id_usuario_vehiculo
            datos['id_vehiculo_dispositivo']= id_vehiculo_dispositivo

            informacion = AdmSolicitud.objects.por_usuariovehiculo_por_vehiculodispositivo(id_usuario_vehiculo,id_vehiculo_dispositivo)
            informacion = AdmSolicitud.objects.por_usuariovehiculo_por_vehiculodispositivo(
    id_usuario_vehiculo, 
    id_vehiculo_dispositivo
).order_by('-iSolicitudID')[:30]
            informacion_serializada = InformacionSolicitudSerializer(instance = informacion , many=True)
            return Response(retorno(status.HTTP_200_OK, 1,'Resultados con éxito', informacion_serializada.data))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al reralizar la solicitud: ' + str(e)))
        
        
class CancelarSolicitudView(generics.UpdateAPIView):
    def post(self,request):
        """Servicio que entrega la información de las solicitudes realizadas por un usuario

        Args:
            id_usuario: int
            id_dispositivo: int
            id_vehiculo: int
            id_solicitud:int

        Returns:
            _type_: _description_
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario = request.data.get('id_usuario')
        id_dispositivo = request.data.get('id_dispositivo')
        id_vehiculo = request.data.get('id_vehiculo')
        id_solicitud = request.data.get('id_solicitud')
        id_usuario_sesion = valida_jwt['usuario_id']
        
        datos = {
            'id_usuario':id_usuario,
            'id_dispositivo':id_dispositivo,
            'id_vehiculo':id_vehiculo,
            'id_solicitud':id_solicitud,
            'id_usuario_sesion':id_usuario_sesion
        }
        serializer = CancelarSolicitudSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, serializer.errors))
        try :
             with transaction.atomic():
                id_usuario_vehiculo = AdmUsuarioVehiculo.objects.por_usuario_por_vehiculo_simple( id_usuario,id_vehiculo).activo().first()
                if not id_usuario:
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'El usuario no tiene el vehículo asignado'))
                    
                id_vehiculo_dispositivo = AdmVehiculoDispositivo.objects.por_vehiculo_por_dispositivo(id_vehiculo,id_dispositivo).activo().first()
                if not id_vehiculo_dispositivo:
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'El vehiculo no tiene el dispositivo asignado'))
                
                solicitud = AdmSolicitud.objects.por_id(id_solicitud).por_usuariovehiculo_por_vehiculodispositivo_pendiente(id_usuario_vehiculo, id_vehiculo_dispositivo)
                
                if not solicitud.exists():
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'La solicitud no se encuentra pendiente, por lo que no se puede cancelar.',solicitud.values()))
                    
                datos['id_usuario_vehiculo']= id_usuario_vehiculo
                datos['id_vehiculo_dispositivo']= id_vehiculo_dispositivo
                datos['estado'] = estadosSolicitud.cancelada
                datos['fecha_proceso'] = datetime.now()
                
                solicitd = AdmSolicitud.cambiar_estado(solicitud.first(),datos)
                return Response(retorno(status.HTTP_200_OK, 1, 'Se canceló la solicitud con éxito'))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al reralizar la solicitud: ' + str(e)  ))
               
        
            
# METODO PAR ADMINISTRADOR 
from rest_framework import generics, status
from rest_framework.response import Response

class ListadoVehiculosConSolicitudesView(generics.GenericAPIView):
    def get(self, request):
        """Metodo que lista todos los vehiculos que tienen solicitudes pendientes"""
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        es_admin = valida_perfil_admin(valida_jwt)
        if not es_admin: 
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
        
        try:
            # Obtiene las solicitudes pendientes
            listado_solicitudes_pendientes = AdmSolicitud.objects.pendientes_annotate().activo()

            # Serializa el queryset
            # listado_vehiculos = ListadoVehiculosConSolicitudesSerializer(
            #     instance=listado_solicitudes_pendientes, many=True
            # )
            
            
            # Retorna la respuesta con los datos serializados
            return Response(retorno(status.HTTP_200_OK, 1, '', listado_solicitudes_pendientes))
        
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al realizar la solicitud: ' + str(e)))
