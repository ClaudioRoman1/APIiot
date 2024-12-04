from rest_framework import serializers

from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.Administracion.AdmUsuarioClientePerfil.Models import AdmUsuarioClientePerfilModel
from Apps.Administracion.AdmUsuarioClientePerfil.Models.AdmUsuarioClientePerfilModel import AdmUsuarioClientePerfil
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos 

class AsignarPerfilUsuarioSerializer(serializers.Serializer):
    id_usuario_cliente  = serializers.IntegerField(required=True,
                                          	error_messages={
                                                            'required': MensajeParametros.parametroRequerido,
                                                            'null': MensajeParametros.parametroRequerido,
                                                            'invalid':MensajeParametros.parametroEntero
                                                            })
    id_perfil  = serializers.IntegerField(required=True,
                                          	error_messages={
                                                            'required': MensajeParametros.parametroRequerido,
                                                            'null': MensajeParametros.parametroRequerido,
                                                            'invalid':MensajeParametros.parametroEntero
                                                            })
    def validate_id_usuario_cliente(self, id_usuario_cliente):
        if not AdmClienteUsuario.objects.por_id(id_usuario_cliente).activo().exists():
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioClienteNoExiste)
        return id_usuario_cliente
    
    def validate(self, data):
        if AdmUsuarioClientePerfil.objects.por_usuario_cliente_por_perfil(data['id_usuario_cliente'], data['id_perfil']).activo().exists():
            raise serializers.ValidationError(MensajeRetornos.mensajePerfilYaAsignado)
        return data

class DesignarPerfilUsuarioSerializer(serializers.Serializer):
    id_cliente_usuario_perfil  = serializers.IntegerField(required=True,
                                          	error_messages={
                                                            'required': MensajeParametros.parametroRequerido,
                                                            'null': MensajeParametros.parametroRequerido,
                                                            'invalid':MensajeParametros.parametroEntero
                                                            })
   
    def validate_id_usuario_cliente(self, id_cliente_usuario_perfil):
        if not AdmUsuarioClientePerfil.objects.por_id(id_cliente_usuario_perfil).activo().exists():
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioClienteNoExiste)
        return id_cliente_usuario_perfil
    

        
