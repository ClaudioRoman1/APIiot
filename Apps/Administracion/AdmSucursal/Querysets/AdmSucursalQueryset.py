from django.db import models


class AdmSucursalQueryset(models.QuerySet):

   def activo(self):
      return self.filter(bActivo=1)

   def por_id(self, sucursalid):
      return self.filter(SucursalID=sucursalid)
