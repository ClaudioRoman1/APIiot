

from rest_framework import serializers

from Apps.Administracion.AdmFlota.Models.AdmFlotaModel import AdmFlota
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos

class ListaVehiculoPorFlotaSerializer(serializers.Serializer):
    id_flota = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':'Debe ser entero',
                                           'required':'Este campo es requerido',
                                           'blank':'Este campo es requerido'
                                       })
    
    def to_representation(self, instance):
        return {
            "id_vehiculo": instance.iVehiculoID,
            "id_flota": instance.iFlotaID_id,
            "nombre_flota":instance.iFlotaID.vcNombre,
            "litros":instance.nCantidadTotalLitros,
            "num_patente":instance.vcPatente
        }
    
class CrearVehiculoSerializer(serializers.Serializer):
    id_flota = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid': MensajeParametros.parametroEntero,
                                            'null':MensajeParametros.parametroRequerido,
                                            'required': MensajeParametros.parametroRequerido,
                                       })
    num_patente = serializers.CharField(required=True,
                                       error_messages={
                                     'null':MensajeParametros.parametroRequerido,
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                       })
    marca = serializers.CharField(required=True,
                                  error_messages={
                                      'null':MensajeParametros.parametroRequerido,
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    cantidad_litros = serializers.DecimalField (required= False , allow_null = True ,
                                                 max_digits=10 , decimal_places=2)
    ano = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid': MensajeParametros.parametroEntero,
                                          'null':MensajeParametros.parametroRequerido,
                                      '     required': MensajeParametros.parametroRequerido,
                                       })
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
    
   
class InformacionVehiculoSerializer(serializers.Serializer):
    id_vehiculo = serializers.IntegerField(required=True,
                                        error_messages={
                                                'invalid':MensajeParametros.parametroEntero,
                                                'required':MensajeParametros.parametroRequerido,
                                                'blank':MensajeParametros.parametroRequerido,
                                        })
    
    def to_representation(self, instance):
        dispositivo = (
            instance.AdmVehiculoDispositivo_AdmVehiculo
            .filter(bActivo=True)
        
        )
        dispositivos =[]
        for item in dispositivo:
            dispositivos.append({
                "id_dispositivo": item.iDispositivoID_id if item else None,
                "codigo_dispositivo": item.iDispositivoID.vcCodigo if item and item.iDispositivoID.vcCodigo is not None else None,
                
            })
        
        flota=instance.iFlotaID
        
        
        return {
            "id_vehiculo":instance.iVehiculoID,
            "marca": instance.vcMarca,
            "patente":instance.vcPatente,
            "cantidad_litros": instance.nCantidadTotalLitros,
            "anio": instance.iAno,
            "dispositivos": dispositivos,
            "flota" :flota.iFlotaID,
            "nombre_flota":flota.vcNombre,
            "id_cliente":flota.iClienteID_id
            
            
            
        }