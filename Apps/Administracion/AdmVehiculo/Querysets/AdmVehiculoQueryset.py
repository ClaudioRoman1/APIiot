
from django.db import models

class AdmVehiculoQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, ivehiculoid):
      return self.filter(iVehiculoID = ivehiculoid)
   
   def por_flota(self,iflotaid):
      return self.filter(iFlotaID = iflotaid)
   
   def por_cliente (self, iclienteid ):
      return self.filter(iFlotaID_iClienteID=iclienteid)
   
   def por_patente(self, patente):
      return self.filter(vcPatente = patente)
   
