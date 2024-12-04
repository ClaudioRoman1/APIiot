from rest_framework import serializers

from Apps.RestBase.Constantes import MensajeParametros

class ListaSucursalesPorClienteSerializer(serializers.Serializer):
    id_cliente = serializers.IntegerField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                    'invalid':MensajeParametros.parametroEntero
                                  })
    id_usuario = serializers.IntegerField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                    'invalid':MensajeParametros.parametroEntero
                                  })