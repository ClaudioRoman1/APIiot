
from django.db import models

class AdmRegionQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, regionid):
      return self.filter(RegionID = regionid)
   
   def por_pais(self,ipaisid):
       return self.filter(iPaisID=ipaisid).activo()