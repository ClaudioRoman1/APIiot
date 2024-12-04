

from rest_framework import serializers

from Apps.Administracion.AdmDispositivo.Models.AdmDispositivoModel import AdmDispositivo
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos

class ListaVehiculoDispositivosSerializer(serializers.Serializer):
    id_cliente = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido,
                                       })
    
    def to_representation(self, instance):
        return {
            "id_dispositivo": instance.iDispositivoID_id,
            "id_vehiculo": instance.iVehiculoID_id,
            "patente":instance.iVehiculoID.vcPatente,
            "flota":instance.iVehiculoID.iFlotaID_id,
            "marca_vehiculo": instance.iVehiculoID.vcMarca,
            "ano": instance.iVehiculoID.iAno
        }

class AsignarDispositivoSerializer(serializers.Serializer):
    id_dispositivo = serializers.IntegerField(required=True,
                                       error_messages={
                                            'invalid':MensajeParametros.parametroEntero,
                                            'required':MensajeParametros.parametroRequerido,
                                            'blank':MensajeParametros.parametroRequerido,
                                       })
    id_vehiculo = serializers.IntegerField(required=True,
                                        error_messages={
                                                'invalid':MensajeParametros.parametroEntero,
                                                'required':MensajeParametros.parametroRequerido,
                                                'blank':MensajeParametros.parametroRequerido,
                                        })
    def validate_id_dispositivo(self,value):
        exists = AdmDispositivo.objects.por_id(value).exists()
        if not exists :
            raise serializers.ValidationError(MensajeRetornos.mensajeErrorNoExiste)
            
        return value
    def validate_id_vehiculo(self,value):
        exists = AdmVehiculo.objects.por_id(value).exists()
        if not exists :
            raise serializers.ValidationError(MensajeRetornos.mensajeErrorNoExiste)
            
        return value
        
class ListaDispositivosAsignadosPorVehiculosSerializer(serializers.Serializer):
    id_vehiculo = serializers.IntegerField(required=True,
                                        error_messages={
                                                'invalid':MensajeParametros.parametroEntero,
                                                'required':MensajeParametros.parametroRequerido,
                                                'blank':MensajeParametros.parametroRequerido,
                                        })
    
    def to_representation(self, instance):
        return {
            "codigo": instance.iDispositivoID.vcCodigo,
            "id_dispositivo": instance.iDispositivoID_id,
            "estado":instance.iDispositivoID.bEstado
        }