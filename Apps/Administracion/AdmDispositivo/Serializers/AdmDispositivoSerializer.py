

from rest_framework import serializers

from Apps.Administracion.AdmDispositivo.Models.AdmDispositivoModel import AdmDispositivo
from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.Administracion.AdmVehiculoDispositivo.Models.AdmVehiculoDispositivoModel import AdmVehiculoDispositivo
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos

class ListaDispositivosSerializer(serializers.Serializer):
    id_cliente = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido
                                       })
    
    def to_representation(self, instance):
        return {
            "id_dispositivo": instance.iDispositivoID,
            "id_tipo_dispositivo": instance.iTipoDispositivoID,
            "estado": instance.bEstado,
        }
        
class CrearDispositivoSerializer(serializers.Serializer):
    id_tipo_dispositivo =  serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido,
                                           'null':MensajeParametros.parametroRequerido
                                           
                                       })
    codigo =  serializers.CharField(required=True,
                                       error_messages={
                                           'null':MensajeParametros.parametroRequerido,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido,
                                      })
    
    def validate_codigo(self,value):
        existe = AdmDispositivo.objects.por_codigo(value).activo().exists()
        if existe :
            raise serializers.ValidationError(MensajeRetornos.mensajeErrorExisteDispositivo)
        return value

class AbrirDispositivoSerializer(serializers.Serializer):
    id_dispositivo =  serializers.IntegerField(required=True,
                                    error_messages={
                                        'invalid':MensajeParametros.parametroEntero,
                                        'required':MensajeParametros.parametroRequerido,
                                        'null':MensajeParametros.parametroRequerido
                                    })
    id_usuario =  serializers.IntegerField(required=True,
                                    error_messages={
                                        'invalid':MensajeParametros.parametroEntero,
                                        'required':MensajeParametros.parametroRequerido,
                                        'null':MensajeParametros.parametroRequerido
                                    })
    id_vehiculo =  serializers.IntegerField(required=True,
                                    error_messages={
                                        'invalid':MensajeParametros.parametroEntero,
                                        'required':MensajeParametros.parametroRequerido,
                                        'null':MensajeParametros.parametroRequerido
                                    })
    
    # def validate(self,value):
    #     dispositivo = AdmDispositivo.objects.por_id(value['id_dispositivo']).activo()
    #     if not dispositivo.exists():
    #         raise serializers.ValidationError(MensajeRetornos.mensajeErrorExisteDispositivo)
    #     vehiculo_dispositivo= AdmVehiculoDispositivo.objects.por_vehiculo_por_dispositivo(value['id_vehiculo'],value['id_dispositivo']).activo()
    #     if not vehiculo_dispositivo.exists():
    #         raise serializers.ValidationError(MensajeRetornos.mensajeErrorExisteDispositivo)
            
    #     vehiculo_usuario = AdmUsuarioVehiculo.objects.por_usuario_por_vehiculo_simple(value['id_usuario'],value['id_vehiculo']).activo()
    #     if not vehiculo_usuario.exists():
    #         raise serializers.ValidationError(MensajeRetornos.mensajeErrorExisteDispositivo)
    
    #     return value
    
    def to_representation(self, instance):
        return {
            "id_dispositivo": instance.iDispositivoID,
            "id_tipo_dispositivo": instance.iTipoDispositivoID,
            "estado": instance.bEstado,
        }
        
class CerrarDispositivoSerializer(serializers.Serializer):
        id_dispositivo =  serializers.IntegerField(required=True,
                                    error_messages={
                                        'invalid':MensajeParametros.parametroEntero,
                                        'required':MensajeParametros.parametroRequerido,
                                        'null':MensajeParametros.parametroRequerido
                                    })
        def to_representation(self, instance):
            return {
                "id_dispositivo": instance.iDispositivoID,
                "id_tipo_dispositivo": instance.iTipoDispositivoID,
                "estado": instance.bEstado,
            }
        
