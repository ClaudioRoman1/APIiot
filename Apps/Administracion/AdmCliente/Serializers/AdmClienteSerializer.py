from django.forms import ValidationError
from rest_framework import serializers

from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.RestBase.Constantes import MensajeParametros

class CrearClienteSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                    'invalid':MensajeParametros.parametroEntero
                                  })
    razon_social = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    identificador = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    nombre_fantasia = serializers.CharField(required=False,
                                            allow_null = True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    
    def validate_identificador(self,identificador):
        if(AdmCliente.objects.filter(vcIdentificador = identificador ).exists()):
            raise ValidationError("El identificador ya está en uso.")
        return identificador
      
        
    