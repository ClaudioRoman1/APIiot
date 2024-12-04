
from django.db import models
from django.db.models import F , Q


class AdmUsuarioVehiculoQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, idispositivoid):
      return self.filter(iDispositivoID= idispositivoid)
   
   def por_cliente(self, iclienteid): 
      return self.select_related(
                  'iUsuarioID',  # Carga el usuario directamente
                  'iVehiculoID'  # Carga el vehículo directamente
            ).prefetch_related(
                  'iVehiculoID__AdmVehiculoDispositivo_AdmVehiculo',  # Carga dispositivos asociados al vehículo
                  'iUsuarioID__ClienteUsuario_Usuario'  # Carga clientes asociados al usuario
            ).filter(iUsuarioID__ClienteUsuario_Usuario__iClienteID=iclienteid)
            
            
      
   # def por_usuario(self,iusuarioid):
   #    return  self.select_related('iUsuarioID').filter(iUsuarioID=iusuarioid)
   def get_queryset(self):
        return AdmUsuarioVehiculoQueryset(self.model, using=self._db)
   def por_usuario(self, iusuarioid):
        # Usamos select_related y prefetch_related para cargar las relaciones necesarias
      retorno=  self.get_queryset().select_related('iUsuarioID', 'iVehiculoID__iFlotaID').prefetch_related(
                'iVehiculoID__AdmVehiculoDispositivo_AdmVehiculo',
                'iUsuarioID__ClienteUsuario_Usuario'
            ).filter(iUsuarioID=iusuarioid)
            
      return retorno
   
   def por_vehiculo(self, ivehiculoid):
      return self.filter(iVehiculoID=ivehiculoid)
   
   def por_usuario_sin_fk(self, iusuarioid):
      
      return self.get_queryset().select_related('iUsuarioID', 'iVehiculoID__iFlotaID','iVehiculoID').filter(iUsuarioID=iusuarioid)
      
   def por_concepto(self, concepto):
      if not concepto:
         return self
      return self.filter(Q(iVehiculoID__iFlotaID__vcNombre__icontains=concepto)| Q(iVehiculoID__vcPatente__icontains=concepto))

   def por_usuario_concepto(self, iusuarioid, concepto):
      retorno = self.por_usuario(iusuarioid=iusuarioid).por_concepto(concepto=concepto)
      return retorno
   
   def por_usuario_por_vehiculo(self,iusuarioid, ivehiculoid):
      retorno  =self.por_usuario(iusuarioid).por_vehiculo(ivehiculoid)
      print(retorno.first())
      return retorno
   def por_usuario_por_vehiculo_simple(self,iusuarioid, ivehiculoid):
      retorno  =self.filter(iUsuarioID = iusuarioid , iVehiculoID= ivehiculoid)
      print(retorno.first())
      return retorno
