
from django.db import models

class AdmPerfilesQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, iperfilid):
      return self.filter(iPerfilID = iperfilid)
   