
from django.db import models

class AdmFlotaQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, iflotaid):
      return self.filter(iFlotaID = iflotaid)
   
   def por_cliente(self, iclienteid):
      return self.filter(iClienteID = iclienteid)
   
