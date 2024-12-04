
from django.db import models

class AdmVehiculoDispositivoQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, idispositivoid):
      return self.filter(iDispositivoid = idispositivoid)
   
   def por_vehiculo(self , ivehiculoid):
      return self.filter(iVehiculoID=ivehiculoid)
   
   def por_cliente(self , iclienteid):
      return self.filter(iVehiculoID__iFlotaID__iClienteID = iclienteid)
   
   def por_dispositivo(self,idispositivoid):
      return self.filter(iDispositivoID= idispositivoid)
   
   def por_vehiculo_por_dispositivo(self, ivehiculoid, idispositivoid):
      return self.por_vehiculo(ivehiculoid=ivehiculoid).por_dispositivo(idispositivoid=idispositivoid)
   
