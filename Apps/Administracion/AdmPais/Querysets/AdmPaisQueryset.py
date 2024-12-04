
from django.db import models

class AdmPaisQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, paisid):
      return self.filter(PaisID = paisid)
   
   def obtener_todos(self):
      return self.all().activo()