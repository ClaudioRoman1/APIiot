from django.db import models
from django.db.models.deletion import PROTECT
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmDominio.Querysets.AdmDominioQueryset import AdmDominioQueryset


class AdmDominio(RestBase):
   DominioID = models.AutoField("Código del registro", primary_key=True)
   vcNombre = models.CharField(max_length=600)
   iDominioPadreID = models.IntegerField(null=True)
   
   objects = AdmDominioQueryset.as_manager()

   class Meta:
      db_table = 'adm_dominio'
      managed = False

   def __str__(self):
      return f' ID del registro: {self.DominioID}'
