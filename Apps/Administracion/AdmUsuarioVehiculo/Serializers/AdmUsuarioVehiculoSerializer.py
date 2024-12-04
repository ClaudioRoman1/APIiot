

from rest_framework import serializers

from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos

class ListaVehiculosAsignadosSerializer(serializers.Serializer):
    id_cliente = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido
                                       })
    
    def to_representation(self, instance):
        dispositivo = instance.iVehiculoID.AdmVehiculoDispositivo_AdmVehiculo.filter(bActivo=True).first()
        cliente=instance.iUsuarioID.ClienteUsuario_Usuario.filter(bActivo=True).first()
        return {
            "id_vehiculo": instance.iVehiculoID_id,
            "patente": instance.iVehiculoID.vcPatente,
            "id_usuario": instance.iUsuarioID_id,
            "nombre_usuario": instance.iUsuarioID.vcNombre,
            "apellidos_usuario": instance.iUsuarioID.vcApellidos,
            "id_dispositivo": dispositivo.iDispositivoID_id if dispositivo else None,
            "codigo_dispositivo":dispositivo.vcCodigo if dispositivo.iDispositivoID.vcCodigo is not None else None,
            "id_cliente": cliente.iClienteID_id
            
        }
        
# class ListaVehiculosAsignadosUsuarioSerializer(serializers.Serializer):
#     id_usuario = serializers.IntegerField(required=True,
#                                        error_messages={
#                                            'invalid':MensajeParametros.parametroEntero,
#                                            'required':MensajeParametros.parametroRequerido,
#                                            'blank':MensajeParametros.parametroRequerido
#                                        })
    
#     def to_representation(self, instance):
#         dispositivo = instance.iVehiculoID.AdmVehiculoDispositivo_AdmVehiculo.filter(bActivo=True).first()
#         flota =instance.iVehiculoID.iFlotaID.AdmVehiculo_AdmFlota.filter(bActivo=True).first()
#         cliente=instance.iUsuarioID.ClienteUsuario_Usuario.filter(bActivo=True).first()
#         return {
#             "id_vehiculo": instance.iVehiculoID_id,
#             "patente": instance.iVehiculoID.vcPatente,
#             "id_usuario": instance.iUsuarioID_id,
#             "nombre_usuario": instance.iUsuarioID.vcNombre,
#             "apellidos_usuario": instance.iUsuarioID.vcApellidos,
#             "id_dispositivo": dispositivo.iDispositivoID_id if dispositivo else None,
#             "codigo_dispositivo":dispositivo.iDispositivoID.vcCodigo if dispositivo.iDispositivoID.vcCodigo is not None else None,
#             "id_cliente": cliente.iClienteID_id,
#             "id_flota":instance.iVehiculoID.iFlotaID,
#             "nombre_flota":instance.iVehiculoID.iFlotaID.vcNombre
            
#         }
        
class ListaVehiculosAsignadosUsuarioSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(
        required=True,
        error_messages={
            'invalid': MensajeParametros.parametroEntero,
            'required': MensajeParametros.parametroRequerido,
            'blank': MensajeParametros.parametroRequerido
        }
    )
    
    def to_representation(self, instance):
        # Obtiene el primer dispositivo activo de forma más eficiente
        dispositivo = (
            instance.iVehiculoID.AdmVehiculoDispositivo_AdmVehiculo
            .filter(bActivo=True)
        
        )
        dispositivos =[]
        for item in dispositivo:
            dispositivos.append({
                "id_dispositivo": item.iDispositivoID_id if item else None,
                "codigo_dispositivo": item.iDispositivoID.vcCodigo if item and item.iDispositivoID.vcCodigo is not None else None,
            })
        
        # Obtiene la primera flota activa relacionada
        flota = (
            instance.iVehiculoID.iFlotaID.AdmVehiculo_AdmFlota
            .filter(bActivo=True)
            .first()
        )

        # Obtiene el cliente activo relacionado
        cliente = (
            instance.iUsuarioID.ClienteUsuario_Usuario
            .filter(bActivo=True)
            .first()
        )

        return {
            "id_vehiculo": instance.iVehiculoID_id,
            "patente": instance.iVehiculoID.vcPatente,
            "id_usuario": instance.iUsuarioID_id,
            "nombre_usuario": instance.iUsuarioID.vcNombre,
            "apellidos_usuario": instance.iUsuarioID.vcApellidos,
            "dispositivo" : dispositivos,
            "id_cliente": cliente.iClienteID_id if cliente else None,
            "id_flota": instance.iVehiculoID.iFlotaID_id,
            "nombre_flota": instance.iVehiculoID.iFlotaID.vcNombre
        }
class BusquedaVehiculosPorUsuarioConceptoSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(
        required=True,
        error_messages={
            'invalid': MensajeParametros.parametroEntero,
            'required': MensajeParametros.parametroRequerido,
            'blank': MensajeParametros.parametroRequerido
        }
    )
    concepto = serializers.CharField(allow_null=True, required=False,allow_blank=True)
    
    def to_representation(self, instance):
        # Obtiene el primer dispositivo activo de forma más eficiente
        dispositivo = (
            instance.iVehiculoID.AdmVehiculoDispositivo_AdmVehiculo
            .filter(bActivo=True)
        
        )
        dispositivos =[]
        for item in dispositivo:
            dispositivos.append({
                "id_dispositivo": item.iDispositivoID_id if item else None,
                "codigo_dispositivo": item.iDispositivoID.vcCodigo if item and item.iDispositivoID.vcCodigo is not None else None,
            })
        
        # Obtiene el cliente activo relacionado
        cliente = (
            instance.iUsuarioID.ClienteUsuario_Usuario
            .filter(bActivo=True)
            .first()
        )

        return {
            "id_vehiculo": instance.iVehiculoID_id,
            "patente": instance.iVehiculoID.vcPatente,
            "id_usuario": instance.iUsuarioID_id,
            "nombre_usuario": instance.iUsuarioID.vcNombre,
            "apellidos_usuario": instance.iUsuarioID.vcApellidos,
            "dispositivo" : dispositivos,
            "id_cliente": cliente.iClienteID_id if cliente else None,
            "id_flota": instance.iVehiculoID.iFlotaID_id,
            "nombre_flota": instance.iVehiculoID.iFlotaID.vcNombre
        }

class AsignarVehiculoUsuarioSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido
                                       })
    id_vehiculo = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido
                                       })
    id_cliente = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':MensajeParametros.parametroEntero,
                                           'required':MensajeParametros.parametroRequerido,
                                           'blank':MensajeParametros.parametroRequerido
                                       })
    
    def validate(self, data):
        vehiculo_asignado  = AdmUsuarioVehiculo.objects.por_usuario_por_vehiculo(data['id_usuario'] , data['id_vehiculo']).activo().exists()
        if not vehiculo_asignado:
            return data
        raise serializers.ValidationError({'id_vehiculo':MensajeRetornos.mensajeErrorVehiculoYaAsignado})
        
    