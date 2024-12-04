from rest_framework import serializers

from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos

class CrearPerfilesSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=True,error_messages = {
        'required': MensajeParametros.parametroRequerido,
        'blank' : MensajeParametros.parametroRequerido,
        'null': MensajeParametros.parametroRequerido
    })
    descripcion = serializers.CharField(required=True,error_messages = {
        'required': MensajeParametros.parametroRequerido,
        'blank' : MensajeParametros.parametroRequerido,
        'null': MensajeParametros.parametroRequerido
    })
    

class ListaPerfilesUsuarioClienteAdministracionSerializer(serializers.Serializer):
    id_usuario_sesion : serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'null':MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                }) # type: ignore
        
    id_usuario = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'null':MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
    id_usuario_cliente = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'null':MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
      
    def validate(self, attrs):
        cliente_usuario= AdmClienteUsuario.objects.por_id(attrs['id_usuario_cliente'])
        if not cliente_usuario.exists():
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioClienteNoExiste)
            
        cliente_usuario_por_usuario = cliente_usuario.por_id_usuario(iusuarioid = attrs['id_usuario'])
        if not cliente_usuario_por_usuario.exists():
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioClienteNoExiste)
        
        return attrs