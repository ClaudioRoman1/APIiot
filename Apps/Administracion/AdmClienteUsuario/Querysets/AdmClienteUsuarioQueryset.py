
from django.db import models

class AdmClienteUsuarioQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, iclienteusuarioid):
      return self.filter(iClienteUsuarioID = iclienteusuarioid)
   
   def clientes_por_id_usuario(self,iusuarioid):
      """Funcion que trae los clientes por id de usuario de un 

      Args:
          iusuarioid (_type_): _description_

      Returns:
          Retorna el id de clientes
      """
      clientes = self.por_id_usuario(iusuarioid)
      id_cliente=[]

      for cliente  in clientes:
            id_cliente.append(cliente.iClienteID_id)
      return id_cliente
   
   def por_id_usuario(self , iusuarioid):
      return self.filter(iUsuarioID =iusuarioid)
   
   def obtiene_cliente_usuario(self , iusuarioid):
      cliente_usuario = self.por_id_usuario(iusuarioid)  
      id_cliente_usuario = [] 
      for usuario  in cliente_usuario:
            id_cliente_usuario.append(usuario.iClienteUsuarioID)
            
      return id_cliente_usuario