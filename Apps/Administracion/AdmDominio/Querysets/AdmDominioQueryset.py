from django.db import models


class AdmDominioQueryset(models.QuerySet):

   def activo(self):
      return self.filter(bActivo=1)

   def por_id(self, dominioid):
      return self.filter(DominioID=dominioid)
