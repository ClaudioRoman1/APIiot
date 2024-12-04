from rest_framework import serializers

from Apps.RestBase.Constantes import MensajeParametros


class CrearCategoriaSerializer(serializers.Serializer):
  nombre_categoria = serializers.CharField(
																					required=True,
																					error_messages={
																					'required': MensajeParametros.parametroRequerido,
																					'null': MensajeParametros.parametroRequerido,
																					'invalid':MensajeParametros.parametroEntero
																					})
  
  imagen_url = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  descripcion_categoria = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class DesactivarCategoriaSerializer(serializers.Serializer):
  id_categoria = serializers.IntegerField(required=True,
                                          	error_messages={
																					'required': MensajeParametros.parametroRequerido,
																					'null': MensajeParametros.parametroRequerido,
																					'invalid':MensajeParametros.parametroEntero
																					})
