
from django.db import models


class AdmUsuarioSucursalQueryset(models.QuerySet):

   def activo(self):
      return self.filter(bActivo=1)

   def por_id(self, empleadoid):
      return self.filter(EmpleadoID=empleadoid)
