from django.db import models
from django.db.models.deletion import PROTECT
from Apps.RestBase.RestBaseModel import RestBase
from Apps.Administracion.AdmPais.Models.AdmPaisModel import AdmPais
from Apps.Administracion.AdmRegion.Querysets.AdmRegionQueryset import AdmRegionQueryset


class AdmRegion(RestBase):
   RegionID = models.AutoField("Código del registro", primary_key=True)
   iPaisID = models.ForeignKey(AdmPais, on_delete=PROTECT, related_name="iPaisID_AdmPais", db_column="iPaisID")
   vcNombre = models.CharField(max_length=80)
   
   objects = AdmRegionQueryset.as_manager()

   class Meta:
      db_table = 'adm_region'
      managed = False