from datetime import datetime
import logging
from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.Administracion.AdmUsuarioVehiculo.Serializers.AdmUsuarioVehiculoSerializer import  AsignarVehiculoUsuarioSerializer, BusquedaVehiculosPorUsuarioConceptoSerializer, ListaVehiculosAsignadosSerializer, ListaVehiculosAsignadosUsuarioSerializer
from Apps.RestBase.Constantes import MensajeRetornos
from Funciones.Encriptacion import valida_token
from Funciones.ObjetoRetorno import retorno
from Funciones.Validaciones import valida_perfil_admin
from django.db import transaction
logger = logging.getLogger('Administracion')
class  ListaVehiculosAsignadosView(generics.ListAPIView):
    def post(self,request):
        """Metodo que muestra lista vehiculos asignados de un cliente
        Retorno: retorno
        Elaborado por: CRoman 13-05-23
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        
        id_cliente = request.data.get('id_cliente')
        id_cliente = request.data.get('id_cliente')
        datos = {
            'id_cliente':id_cliente
        }
        serializer = ListaVehiculosAsignadosSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializer.errors ))
        
        try:
            vehiculos = AdmUsuarioVehiculo.objects.por_cliente(iclienteid = id_cliente).activo()
            ls_vehiculos = list(vehiculos)
            
            if len(ls_vehiculos) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay vehiculos ', None,None))
        
            lista_vehiculos = ListaVehiculosAsignadosSerializer(instance=vehiculos,many=True)
            lista_vehiculos_serializadas= lista_vehiculos.data 
            total_reg = len(lista_vehiculos_serializadas)
        
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_vehiculos_serializadas, total_reg ))
        except Exception as e:
            logger.error(f'Error en la vista POST ListaVehiculosAsignadosView: {str(e)}')  
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al intentar realizar busqueda' + str(e) ))
        
            
        
        
# class ListaVehiculosAsignadosUsuarioView(generics.ListAPIView):
#     def post(self , request): 
#         """Servicio que lista todos los vehiculos asignados a un usuario en especifico
#         Args:
#             id_usuario (int): id del usuario en sesión o uno que decida el admin
#         Returns:
#             List
#         """
#         valida_jwt = valida_token(request)
#         if valida_jwt['mensaje'] != 'valido':
#             return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        
             
#         es_admin = valida_perfil_admin(valida_jwt)
        
#         if  es_admin:
#             id_usuario = request.data.get('id_usuario')
#         else:
#             id_usuario = valida_jwt['usuario_id']
            
#         datos={}
#         datos['id_usuario']= id_usuario
#         datos['id_usuario_sesion'] = valida_jwt['usuario_id']

#         serializer = ListaVehiculosAsignadosUsuarioSerializer(data=datos)
#         if not serializer.is_valid():
#             return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializer.errors ))
        
#         try:
#             vehiculos = AdmUsuarioVehiculo.objects.por_usuario(iusuarioid = id_usuario).activo()
#             ls_vehiculos = list(vehiculos)
            
#             if len(ls_vehiculos) ==0:
#                 return Response(retorno(status.HTTP_200_OK, 0, 'No hay vehiculos asignados al usuario ', None,None))
        
#             lista_vehiculos = ListaVehiculosAsignadosUsuarioSerializer(instance=vehiculos,many=True)
#             lista_vehiculos_serializadas= lista_vehiculos.data 
#             total_reg = len(lista_vehiculos_serializadas)
        
        
#             return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_vehiculos_serializadas, total_reg ))
#         except Exception as e:
#             logger.error(f'Error en la vista POST ListaVehiculosAsignadosUsuarioView: {str(e)}')  
#             return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al intentar realizar busqueda' + str(e) ))
            

class ListaVehiculosAsignadosUsuarioView(generics.ListAPIView):
    def post(self, request):
        """Servicio que lista todos los vehiculos asignados a un usuario en especifico

        Args:
            id_usuario (int): solo si es admiinstrador lo solicita , sino lo saca desde el mismo token

        Returns:
            Lista de vehiculos
        """
        # Verificación de token, perfil, y extracción de usuario similar a tu código actual
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))

        es_admin = valida_perfil_admin(valida_jwt)
        id_usuario = request.data.get('id_usuario') if es_admin else request.data.get('id_usuario') if  request.data.get('id_usuario') else alida_jwt['usuario_id']
        
        datos = {
            'id_usuario': id_usuario,
            'id_usuario_sesion': valida_jwt['usuario_id']
        }

        serializer = ListaVehiculosAsignadosUsuarioSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializer.errors))

        try:
            vehiculos = AdmUsuarioVehiculo.objects.por_usuario(iusuarioid=id_usuario).activo()
            if not vehiculos.exists():
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay vehiculos asignados al usuario', None, None))

            lista_vehiculos = ListaVehiculosAsignadosUsuarioSerializer(instance=vehiculos, many=True)
            lista_vehiculos_serializadas = lista_vehiculos.data
            total_reg = len(lista_vehiculos_serializadas)
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso', lista_vehiculos_serializadas, total_reg))
        except Exception as e:
            logger.error(f'Error en la vista POST ListaVehiculosAsignadosUsuarioView: {str(e)}')
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, f'Error al intentar realizar busqueda: {str(e)}'))

class AsignarVehiculoUsuarioView(generics.CreateAPIView):
    def post(self,request):
        """Servicio que permite asignarle un vehiculo a un usuario 

        Args:
            id_vehiculo(int): id del vehiculo que se le asignará al usuario
            id_usuario(int): id del usuario a quien se le asignará un vehículo
        Return : 
            id_vehiculo_usuario(int) : Registro en base de datos
        """
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        
        es_admin = valida_perfil_admin(valida_jwt)
        
        if not es_admin:
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, MensajeRetornos.mensajeNoEsAdmin))
        
        id_usuario = request.data.get('id_usuario')
        id_cliente = request.data.get('id_cliente')
        id_vehiculo = request.data.get('id_vehiculo')
        
        datos={}
        datos['id_usuario']= id_usuario
        datos['id_cliente']= id_cliente
        datos['id_vehiculo']= id_vehiculo

        serializer = AsignarVehiculoUsuarioSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializer.errors ))
        
        try:
            with transaction.atomic():
                datos['id_usuario_sesion'] = valida_jwt['usuario_id']
                datos['fecha_proceso'] = datetime.now()
                
                asignacion = AdmUsuarioVehiculo.asignar(AdmUsuarioVehiculo, datos)
          
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Creación exitosa', ))
        except Exception as e:
            logger.error(f'Error en la vista POST AsignarVehiculoUsuarioView: {str(e)}')  
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al asignar un vehiculo al usuario' + str(e) ))
        

class BusquedaVehiculosPorUsuarioConceptoView(generics.ListAPIView):
    def post(self,request):
        valida_jwt = valida_token(request)
        if valida_jwt['mensaje'] != 'valido':
            return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje']))
        
        id_usuario = request.data.get('id_usuario')
        concepto = request.data.get('concepto')
        
        
        datos={}
        datos['id_usuario']= id_usuario
        datos['concepto']= concepto

        serializer = BusquedaVehiculosPorUsuarioConceptoSerializer(data=datos)
        if not serializer.is_valid():
            return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializer.errors ))
        
        try:   
            vehiculos = AdmUsuarioVehiculo.objects.por_usuario_concepto( id_usuario, concepto) 
            ls_vehiculos = list(vehiculos)
            
            if len(ls_vehiculos) ==0:
                return Response(retorno(status.HTTP_200_OK, 1, [], None,None))
        
            lista_vehiculos = BusquedaVehiculosPorUsuarioConceptoSerializer(instance=vehiculos,many=True)
            lista_vehiculos_serializadas= lista_vehiculos.data 
            total_reg = len(lista_vehiculos_serializadas)

            return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeBusquedaOk,lista_vehiculos_serializadas, total_reg ))
        except Exception as e:
            logger.error(f'Error en la vista POST BusquedaVehiculosPorUsuarioConceptoView: {str(e)}')  
            return Response(retorno(status.HTTP_500_INTERNAL_SERVER_ERROR, 0, 'Error al asignar un vehiculo al usuario' + str(e) ))
        
