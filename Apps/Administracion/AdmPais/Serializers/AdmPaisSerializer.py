
from rest_framework import serializers

class ListaPaisesSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True)
    
    def to_representation(self, instance):
        return {
            "id_pais": instance.PaisID,
            "nombre": instance.vcNombre,
            "codigo_area": int(instance.vcCodigoAreaPais)
        }
    