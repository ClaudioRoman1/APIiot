
from django.db import models

class AdmDispositivoQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, idispositivoid):
      return self.filter(iDispositivoID = idispositivoid)
   
   def por_codigo(self,vccodigo):
      return self.filter(vcCodigo=  vccodigo)
   
   def por_vehiculo(self,ivehiculoid):
      resultado = self.filter(AdmVehiculoDispositivo_AdmDispositivo__iVehiculoID_id=ivehiculoid)
      return resultado
   
   def por_usuario(self,iusuarioid):
      resultado =self.filter(AdmVehiculoDispositivo_AdmDispositivo__AdmVehiculoDispositivo_AdmVehiculo__AdmUsuarioVehiculo_AdmVehiculo__iUsuarioID_id= iusuarioid)
      return resultado
   
   
   def vehiculo_dispositivo_por_id(self,idispositivoid):
      resultado=self.select_related('AdmVehiculoDispositivo_AdmDispositivo').filter(iDispositivoID=idispositivoid).first()
      return resultado
   
   def vehiculo_dispositivo_por_vehiculo_id(self,ivehiculoid):
      resultado=self.select_related('AdmVehiculoDispositivo_AdmVehiculo').filter(iVehiculoID=ivehiculoid).activo()
      return resultado
   def por_id_por_usuario_por_vehiculo(self,idispositivoid,iusuarioid,ivehiculoid):
      return self.vehiculo_dispositivo_por_id(idispositivoid).vehiculo_dispositivo_por_vehiculo_id(ivehiculoid)
      #   AdmVehiculoDispositivo_AdmDispositivo__AdmVehiculoDispositivo_AdmVehiculo__AdmUsuarioVehiculo_AdmVehiculo__iUsuarioID=iusuarioid
   
