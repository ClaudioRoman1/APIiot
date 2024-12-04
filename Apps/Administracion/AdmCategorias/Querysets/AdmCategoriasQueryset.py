from django.db import models


class AdmCategoriasQueryset(models.QuerySet):

   def activo(self):
      return self.filter(bActivo=1)

   def por_id(self, categoriaid):
      return self.filter(pk__exact=categoriaid)
   
   def por_id_activo(self, categoriaid):
      return self.por_id(categoriaid=categoriaid).activo()
