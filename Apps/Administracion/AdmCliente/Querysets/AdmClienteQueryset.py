
from django.db import models

class AdmClienteQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, clienteid):
      return self.filter(ClienteID = clienteid)