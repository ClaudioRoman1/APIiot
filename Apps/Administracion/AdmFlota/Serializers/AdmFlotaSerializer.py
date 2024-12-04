

from rest_framework import serializers

class ListaFlotaSerializer(serializers.Serializer):
    id_cliente = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':'Debe ser entero',
                                           'required':'Este campo es requerido',
                                           'blank':'Este campo es requerido'
                                       })
    
    def to_representation(self, instance):
        return {
            "id_flota": instance.iFlotaID,
            "id_cliente": instance.iClienteID_id,
            "identificador_cliente": instance.iClienteID.vcIdentificador,
            "razon_social_cliente": instance.iClienteID.vcRazonSocial,
            "nombre_fantasia_cliente":instance.iClienteID.vcNombreFantasia,
            "bEstadoRegistro" : instance.iClienteID.bEstadoRegistro
        }
    