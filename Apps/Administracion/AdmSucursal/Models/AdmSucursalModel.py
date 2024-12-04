from django.db import models
from django.db.models.deletion import PROTECT
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmSucursal.Querysets.AdmSucursalQueryset import AdmSucursalQueryset


class AdmSucursal(RestBase):
   SucursalID = models.AutoField("Código del registro", primary_key=True)
   vcNombre = models.CharField(max_length=80)
   vcCalle= models.CharField(max_length=35 , null=True)

   objects = AdmSucursalQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Sucursal'
      managed = False

   def __str__(self):
      return f' ID del registro: {self.SucursalID}'

   def crear_sucursal(self, datos):

        return self.objects.create(
                vcNombre=datos['nombre_sucursal'],
                iPaisID_id = datos['id_pais'],
                vcCalle = datos['calle'] if 'calle' in datos else None,
                bActivo=1, 
                dtmCreacion=datos['fecha_proceso'],
                iUsuarioCreacionID=datos['id_usuario_sesion']
            )
        