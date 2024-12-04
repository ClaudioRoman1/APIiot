from rest_framework import serializers

from Apps.RestBase.Constantes import MensajeParametros


class AsignarUsuarioSucursalViewSerializer(serializers.Serializer):
	id_usuario = serializers.IntegerField(
   													required=True,
                            error_messages={
																'required': MensajeParametros.parametroRequerido,
																'null': MensajeParametros.parametroRequerido,
																'invalid':MensajeParametros.parametroEntero
                            	})
	id_sucursal = serializers.IntegerField(
   													required=True,
                            error_messages={
																'required': MensajeParametros.parametroRequerido,
																'null': MensajeParametros.parametroRequerido,
																'invalid':MensajeParametros.parametroEntero
                            	})


def to_representation(self, instance):
	return {
					'id_comuna': instance.ComunaID,
					'nombre_comuna':instance.vcNombre
					}
