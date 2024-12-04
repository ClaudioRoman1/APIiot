
from django.db import models


class AdmUsuarioQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, usuarioid):
      return self.filter(iUsuarioID = usuarioid)
   
   
   def por_correo(self,correo_electronico):
      return self.filter(vcCorreoElectronico=correo_electronico).activo()
   
   def por_contraseña(self, contraseña):
      return self.filter(vcContrasena = contraseña).activo()
   
   def por_usuario_contraseña(self, email,password):
      return self.por_correo(correo_electronico=email).por_contraseña(contraseña=password)
   
   def por_rut(self, identificador):
      return self.filter(vcIdentificador = identificador).activo()
   
   def por_id_rut(self,id_usuario , rut):
      return self.por_id(usuarioid=id_usuario).por_rut(identificador=rut).activo()

   
   def obtiene_cliente_usuario(self , usuario):
      cliente_usuario = usuario.ClienteUsuario_Usuario.values()
      if not cliente_usuario.exists():
         id_cliente_usuario = None
      if len(cliente_usuario)==1:# Suponiendo que un usuario puede tener solo un ClienteUsuario
         cliente_usuario = cliente_usuario.first()
         id_cliente_usuario = cliente_usuario.iClienteUsuarioID
      elif len(cliente_usuario > 1):
         for usuario  in cliente_usuario:
            id_cliente_usuario.append(usuario.iClienteUsuarioID)
            
      return id_cliente_usuario
   
   
   
