from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmFlota.Querysets.AdmFlotaQueryset import AdmFlotaQueryset
from Apps.RestBase.RestBaseModel import RestBase


class AdmFlota(RestBase):
   iFlotaID = models.AutoField("Código del registro", primary_key=True)
   iClienteID = models.ForeignKey(AdmCliente, on_delete=PROTECT, related_name="AdmFlota_AdmCliente", db_column="iClienteID")
   vcNombre = models.CharField(max_length=80)
   
   objects = AdmFlotaQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Flota'
      managed = False