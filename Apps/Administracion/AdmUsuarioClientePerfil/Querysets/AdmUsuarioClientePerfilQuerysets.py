
from django.db import models
from django.db.models import F

class AdmUsuarioClientePerfilQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, iusuarioclienteperfilid):
      return self.filter(iUsuarioClientePerfilID = iusuarioclienteperfilid)
   
   def por_cliente_usuario(self,iusuarioclienteid):
      return self.filter(iClienteUsuarioID =iusuarioclienteid )
   def por_perfil(self, iperfilid):
      return self.filter(iPerfilID = iperfilid)
   
   def por_cliente_usuario_por_perfil(self , iusuarioclienteid,iperfilid):
       usuario_cliente = self.por_cliente_usuario(iusuarioclienteid)
       usuario_cliente_perfil = usuario_cliente.por_perfil(iperfilid)
       return usuario_cliente_perfil
    
   def por_cliente_usuario_anotate(self,iusuarioclienteid):
      return self.por_cliente_usuario(iusuarioclienteid).activo().annotate(
         id_usuario_cliente_perfil = F('iUsuarioClientePerfilID'),
         id_usuario_cliente = F('iClienteUsuarioID_id'),
         id_perfil = F('iPerfilID_id'),
         nombre  = F('iPerfilID__vcNombre'),
         descripcion = F('iPerfilID__vcDescripcion')
      ).values(
         'id_usuario_cliente_perfil','id_usuario_cliente','id_perfil','nombre',
         'descripcion'
      )
   
  