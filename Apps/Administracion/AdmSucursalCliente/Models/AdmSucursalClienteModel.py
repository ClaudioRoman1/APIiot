from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmSucursal.Models.AdmSucursalModel import AdmSucursal
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmSucursalCliente.Querysets.AdmSucursalClienteQueryset import AdmSucursalClienteQueryset


class AdmSucursalCliente(RestBase):
   iSucursalClienteID = models.AutoField("Código del registro", primary_key=True)
   iClienteID = models.ForeignKey(AdmCliente, on_delete=PROTECT, related_name="SucursalCliente_Cliente", db_column="iClienteID")
   iSucursalID = models.ForeignKey(AdmSucursal, on_delete=PROTECT, related_name="SucursalCliente_Sucursal", db_column="iSucursalID")
   
   objects = AdmSucursalClienteQueryset.as_manager()

   class Meta:
      db_table = 'adm_sucursalcliente'
      managed = False

   def __str__(self):
      return f' ID del registro: {self.iSucursalClienteID}'
  
   def crear_sucursal_cliente(self,datos, sucursal):
       sucursal_cliente =  AdmSucursalCliente.objects.create(
          iClienteID_id = datos['id_cliente'],
          iSucursalID =  sucursal,
          iUsuarioCreacionID = datos['id_usuario_sesion'],
          dtmCreacion = datos['fecha_proceso'],
          bActivo = 1
       )
       return sucursal_cliente