from rest_framework import serializers
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.RestBase.Constantes import MensajeParametros, MensajeRetornos
from django.contrib.auth.hashers import make_password, check_password


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    password = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })

    
class CrearUsuarioSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                      'null':MensajeParametros.parametroRequerido
                                  })
    apellidos = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                      'null':MensajeParametros.parametroRequerido
                                  })
    identificador = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                      'null':MensajeParametros.parametroRequerido
                                  })
    num_cel = serializers.CharField(required=True,
                                       allow_null =True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'null':MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                      })
    correo_electronico = serializers.EmailField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })
    id_pais = serializers.IntegerField(required=True,
                                       allow_null =True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                    'invalid':MensajeParametros.parametroEntero
                                  })


    direccion  = serializers.CharField(required=True,
                                       allow_null =True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })

    contrasena = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })

    
    def validate(self,attrs):
        existe_por_correo = AdmUsuario.objects.por_correo(attrs['correo_electronico']).first()
        existe_por_rut = AdmUsuario.objects.por_rut(attrs['identificador']).first()
        if existe_por_correo:
            raise serializers.ValidationError(MensajeRetornos.mensajeCorreoExiste)
        if existe_por_rut:
            raise serializers.ValidationError(MensajeRetornos.mensajeRutExiste)
        return attrs
    
class CrearUsuarioClienteSerializer(CrearUsuarioSerializer):
    id_cliente= serializers.IntegerField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido,
                                    'invalid':MensajeParametros.parametroEntero,
                                    'null':MensajeParametros.parametroEntero
                                  })
    def validate_id_cliente(self,id_cliente):
        if not AdmCliente.objects.por_id(id_cliente).activo().exists():
            raise serializers.ValidationError(MensajeRetornos.mensajeClienteNoExiste)
        return id_cliente
    
    

    
class ActivarUsuarioSerializer(serializers.Serializer):
    id_usuario_activar = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
    
    def validate(self , data):
        usuario = AdmUsuario.objects.por_id(data['id_usuario_activar']).first()
        if usuario is None:
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioNoExiste)            
        if usuario.bActivo == True:
            raise serializers.ValidationError(MensajeRetornos.mensajeUsuarioActivo)  
        return data

    
class DesactivarUsuarioSerializer(serializers.Serializer):
    id_usuario_desactivar = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
    
    

    
class ValidaEmailSerializer(serializers.Serializer):
    correo_electronico = serializers.EmailField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })

    
class ValidaRutSerializer(serializers.Serializer):
    identificador = serializers.CharField(required=True,
                                  error_messages={
                                      'required': MensajeParametros.parametroRequerido,
                                      'blank': MensajeParametros.parametroRequerido
                                  })


class EditarUsuarioSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })
    apellidos = serializers.CharField(required=False, allow_blank=True, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })
    num_cel = serializers.CharField(required=False, allow_blank=True, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })
    correo_electronico = serializers.EmailField(required=False, allow_blank=True, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })
    id_pais = serializers.IntegerField(required=False, allow_null=True, error_messages={
        'invalid': MensajeParametros.parametroEntero
    })
    direccion = serializers.CharField(required=False, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })
    contrasena = serializers.CharField(required=False, error_messages={
        'required': MensajeParametros.parametroRequerido,
        'blank': MensajeParametros.parametroRequerido
    })
    identificador =serializers.CharField(required=False, allow_blank=True, allow_null=True, error_messages={
        'blank': MensajeParametros.parametroRequerido
    })

    # id_rol = serializers.IntegerField(required=False,
    #                               error_messages={
    #                                   'required': MensajeParametros.parametroRequerido,
    #                                   'blank': MensajeParametros.parametroRequerido,
    #                                 'invalid':MensajeParametros.parametroEntero
    #                               })


class IniciaSesiónClienteSerializer(serializers.Serializer):
      id_usuario = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
      id_cliente = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
      
      
class SelectorClienteUsuarioSerializer(serializers.Serializer):
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
        
class CambiarContrasenaSerializer(serializers.Serializer):
    antigua_contrasena = serializers.CharField(write_only=True, required=True)
    nueva_contrasena = serializers.CharField(write_only=True, required=True)
    id_usuario = serializers.IntegerField(required=True,
                                                error_messages={
                                                'required': MensajeParametros.parametroRequerido,
                                                'blank': MensajeParametros.parametroRequerido,
                                                'null':MensajeParametros.parametroRequerido,
                                                'invalid':MensajeParametros.parametroEntero
                                                })
    
    def validate_antigua_contrasena(self, value):
        is_match = check_password(value,self.context['usuario'].vcContrasena)
        if not is_match:
            raise serializers.ValidationError("La contraseña anterior es incorrecta.")
        return value

  

    def validate_nueva_contrasena(self, value):
        # Usar validadores de contraseña predeterminados de Django
        is_match = check_password(value,self.context['usuario'].vcContrasena)
        if  is_match:
            raise serializers.ValidationError("La contraseña ya fue utilizada")
        
        return value
class InformacionPersonalSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return{
            'id_usuario': instance.iUsuarioID,
            'nombre':instance.vcNombre,
            'apellidos': instance.vcApellidos,
            'identificador': instance.vcIdentificador,
            'pais': instance.iPaisID.vcNombre if  instance.iPaisID_id  is not None else None,
            'num_cel': instance.vcNumeroMovil if  instance.vcNumeroMovil  is not None else None,
            'direccion': instance.vcDireccion if  instance.vcDireccion  is not None else None,
            'identificador': instance.vcIdentificador if  instance.vcIdentificador  is not None else None,
            'correo_electronico':instance.vcCorreoElectronico
            
        }
        # return super().to_representation(instance)