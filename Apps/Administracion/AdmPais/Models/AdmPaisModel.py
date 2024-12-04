from django.db import models

# Create your models here.from django.db import models
from django.db.models.deletion import PROTECT
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmPais.Querysets.AdmPaisQueryset import AdmPaisQueryset


class AdmPais(RestBase):
   iPaisID = models.AutoField("Código del registro", primary_key=True)
   vcNombre = models.CharField(null=True, max_length=40)
   # vcCodigoAreaPais = models.FloatField(null=True)
   
   objects = AdmPaisQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Pais'
      managed = False



