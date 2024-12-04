

from rest_framework import serializers

class ListaRegionesSerializer(serializers.Serializer):
    id_pais = serializers.IntegerField(required=True,
                                       error_messages={
                                           'invalid':'Debe ser entero',
                                           'required':'Este campo es requerido',
                                           'blank':'Este campo es requerido'
                                       })
    
    def to_representation(self, instance):
        return {
            "id_region": instance.RegionID,
            "nombre_region": instance.vcNombre,
        }
    