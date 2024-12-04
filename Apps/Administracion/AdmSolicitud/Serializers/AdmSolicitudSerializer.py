

import json
from rest_framework import serializers

from Apps.Administracion.AdmFlota.Models.AdmFlotaModel import AdmFlota
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos


    
class SolicitudAbrirDispositivoSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid': MensajeParametros.parametroEntero,
                                            'null':MensajeParametros.parametroRequerido,
                                            'required': MensajeParametros.parametroRequerido,
                                       })
    id_dispositivo = serializers.IntegerField(required=True,
                                       error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                       })
    id_vehiculo = serializers.IntegerField(required=True,
                                  error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                  })
    imagenes = serializers.JSONField (required= False , allow_null = True ,
                                               error_messages={
                                                'invalid': MensajeParametros.parametroJson,
                                                   
                                               } )

    def validate_id_flota(self,value):
        existe_flota = AdmFlota.objects.por_id(value).activo().exists()
        if not existe_flota:
            raise serializers.ValidationError(MensajeRetornos.mensajeErrorNoExiste)
        return value
    def validate_num_patente(self,value):
        existe_patente = AdmVehiculo.objects.por_patente(value.upper()).activo().exists()
        if  existe_patente:
            raise serializers.ValidationError(MensajeRetornos.mensajeErrorExistePatente)
        return value
    
    def to_representation(self, instance):
        params ={
            "id_flota":instance.iFlotaID,
            "id_cliente": instance.iFlotaID.iClienteID,
            'num_patente' : instance.vcPatente,
            "marca" : instance.vcMarca,
            "ano" : instance.ano,
            "fecha_creacion": instance.dtmCreacion
        }
        return super().to_representation(params)

class InformacionSolicitudSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid': MensajeParametros.parametroEntero,
                                            'null':MensajeParametros.parametroRequerido,
                                            'required': MensajeParametros.parametroRequerido,
                                       })
    id_dispositivo = serializers.IntegerField(required=True,
                                       error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                       })
    id_vehiculo = serializers.IntegerField(required=True,
                                  error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                  })

    def to_representation(self, instance):
    # Validar y procesar 'jImagenes'
        imagenes = None
        imagenes  = instance.jImagenes
            
        

        
        # Retornar la representación serializada
        return {
            "id_solicitud": instance.iSolicitudID,
            "id_usuario_vehiculo": instance.iUsuarioVehiculoID_id,
            "id_vehiculo_disipositivo": instance.iVehiculoDispositivoID_id,
            "estado": instance.bEstado,
            "imagenes":imagenes,
            "fecha_anulacion": instance.dtmAnulacion,
            "id_usuario_anulacion": instance.iUsuarioAnulacionID,
            "fecha_modificacion": instance.dtmUltimaModificacion,
            "fecha_solicitud": instance.dtmCreacion,
            "id_usuario_creacion": instance.iUsuarioCreacionID,
            "id_usuario_modificacion": instance.iUsuarioUltimaModificacionID,
            "activo": instance.bActivo,
        }

        # return {
        #     "id_solicitud":instance.iSolicitudID,
        #     "id_usuario_vehiculo":instance.iUsuarioVehiculoID_id,
        #     "id_vehiculo_disipositivo":instance.iVehiculoDispositivoID_id,
        #     "imagenes":imagenes ,
        #     "estado":instance.bEstado,
        #     "fecha_anulacion":instance.dtmAnulacion,
        #     "id_usuario_anulacion":instance.iUsuarioAnulacionID,
        #     "fecha_modificacion":instance.dtmUltimaModificacion,
        #     "fecha_solicitud":instance.dtmCreacion,
        #     "id_usuario_creacion":instance.iUsuarioCreacionID,
        #     "id_usuario_modificacion":instance.iUsuarioUltimaModificacionID,
        #     "activo":instance.bActivo
        # }
        
class CancelarSolicitudSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid': MensajeParametros.parametroEntero,
                                            'null':MensajeParametros.parametroRequerido,
                                            'required': MensajeParametros.parametroRequerido,
                                       })
    id_dispositivo = serializers.IntegerField(required=True,
                                       error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                       })
    id_vehiculo = serializers.IntegerField(required=True,
                                  error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                  })
    id_solicitud = serializers.IntegerField(required=True,
                                  error_messages={
                                        'invalid': MensajeParametros.parametroEntero,
                                        'null':MensajeParametros.parametroRequerido,
                                        'required': MensajeParametros.parametroRequerido,
                                  })

class ListadoVehiculosConSolicitudesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # `instance` aquí es un solo objeto de solicitud, así que lo representamos directamente
        return {
            'id_solicitud': instance.iSolicitudID,
            'id_vehiculo_dispositivo': instance.iVehiculoDispositivoID.iVehiculoID
        }

    
