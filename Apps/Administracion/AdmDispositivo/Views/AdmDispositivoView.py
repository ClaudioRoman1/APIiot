from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmDispositivo.Models.AdmDispositivoModel import AdmDispositivo
from Apps.Administracion.AdmDispositivo.Serializers.AdmDispositivoSerializer import AbrirDispositivoSerializer, CerrarDispositivoSerializer, CrearDispositivoSerializer, ListaDispositivosSerializer
from Apps.Administracion.AdmSolicitud.Models.AdmSolicitudModel import AdmSolicitud
from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.Administracion.AdmVehiculoDispositivo.Models.AdmVehiculoDispositivoModel import AdmVehiculoDispositivo
from Apps.RestBase.Constantes import estadosSolicitud
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction

class  ListaDispositivosView(generics.ListAPIView):
    """Metodo que muestra la dispositivos por cliente
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        id_cliente = request.data.get('id_cliente')
        datos = {
            'id_cliente':id_cliente
        }
        serializador = ListaDispositivosSerializer(data=datos)
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))
        try:
            dispositivos = AdmDispositivo.objects.por_cliente(iclienteid = id_cliente).activo()
            ls_dispositivos = list(dispositivos)
            
            if len(ls_dispositivos) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay dispositivos ', None,None))
        
            lista_dispositivos = ListaDispositivosSerializer(instance=dispositivos,many=True)
            lista_dispositivos_serializadas= lista_dispositivos.data 
            total_reg = len(lista_dispositivos_serializadas)
        
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_dispositivos_serializadas, total_reg ))
        except Exception as e :
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, str(e) ))
            
        
class CrearDispositivoView(generics.CreateAPIView):
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        codigo = request.data.get('codigo')
        id_tipo_dispositivo = request.data.get('id_tipo_dispositivo')
        
        datos={}
        datos['codigo'] = codigo
        datos['id_tipo_dispositivo'] = id_tipo_dispositivo
        
        serializador = CrearDispositivoSerializer(data=datos)
        
        if not serializador.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))
        
        try: 
            with transaction.atomic():
                datos['fecha_proceso'] = datetime.now()
                datos['id_usuario_sesion']=valida_jwt['usuario_id']
                dispositivo = AdmDispositivo.crear(AdmDispositivo,datos)
                resultado={}
                resultado['id_dispositivo'] = dispositivo.iDispositivoID
                return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',resultado, 1 ))
                
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, str(e) ))
        
class AbrirDispositivoView(generics.UpdateAPIView):
    def post(self,request):
        """Método que abre el dispositivo

        Args:
            id_dispositivo (int): id del dispossitivo
            id_usuario_sesion : id del usuario de sesión
            id_vehiculo : id del vehículo que se encuentra el dispositivo
            id_solicitud:id de la solicitud realizada por el usuario
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_usuario = request.data.get('id_usuario')
        id_dispositivo = request.data.get('id_dispositivo')
        id_vehiculo = request.data.get('id_vehiculo')
        id_usuario_sesion = valida_jwt['usuario_id']
        id_solicitud = request.data.get('id_solicitud')
        
        datos = {
            'id_usuario':id_usuario,
            'id_dispositivo':id_dispositivo,
            'id_vehiculo':id_vehiculo,
            'id_usuario_sesion':id_usuario_sesion,
            'id_solicitud':id_solicitud
            
        }
        serializer = AbrirDispositivoSerializer(data=datos)
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
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'La solicitud no está pendiente'))
                    
                dispositivo = AdmDispositivo.objects.por_id(id_dispositivo).first()
                datos['estado']= estadosSolicitud.aceptada
                datos['fecha_proceso'] = datetime.now()
                solicitud = AdmSolicitud.cambiar_estado(solicitud.first(),datos)
                dispositivo_actualizado = AdmDispositivo.abrir(dispositivo,datos)
                dispositivo_serializado = AbrirDispositivoSerializer(instance=dispositivo_actualizado)
                return Response(retorno(status.HTTP_200_OK, 1, 'El dispositivo se ha abierto con éxito',dispositivo_serializado.data, 1 ))
                # return Response(retorno(status.HTTP_200_OK, 1, 'Solicitud creada con éxito'))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al reralizar la solicitud: ' + str(e)  ))
        
        
class CerrarDispositivoView(generics.UpdateAPIView):
    def post(self,request):
        """Método que cierra el dispositivo

        Args:
            id_dispositivo (int): id del dispossitivo
            id_usuario_sesion : id del usuario de sesión
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
        
        id_dispositivo = request.data.get('id_dispositivo')
        id_usuario_sesion = valida_jwt['usuario_id']
        
        datos = {
            'id_dispositivo':id_dispositivo,
            'id_usuario_sesion':id_usuario_sesion,
        }
        serializer = CerrarDispositivoSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, serializer.errors))
        try : 
            with transaction.atomic():
                dispositivo = AdmDispositivo.objects.por_id(id_dispositivo).first()
                if dispositivo.bEstado!=True :
                    return Response(retorno(status.HTTP_400_BAD_REQUEST, 0,'El dispositivo ya se encuentra cerrado'))
                datos['fecha_proceso'] = datetime.now()
                dispositivo_actualizado = AdmDispositivo.cerrar(dispositivo,datos)
                dispositivo_serializado = CerrarDispositivoSerializer(instance=dispositivo_actualizado)
                return Response(retorno(status.HTTP_200_OK, 1, 'El dispositivo se ha cerrado',dispositivo_serializado.data, 1 ))
        except Exception as e:
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al reralizar la solicitud:' + str(e)  ))
        
        
        
        


