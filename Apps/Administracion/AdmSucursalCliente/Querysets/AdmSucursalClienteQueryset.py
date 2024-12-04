
from django.db import models
from django.db.models import  F


class AdmSucursalClienteQueryset(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = 1)

   def por_id(self, sucursalclienteid):
      return self.filter(iSucursalClienteID = sucursalclienteid)
   
   def por_id_cliente(self, iclienteid):
      sucursales = self.filter(iClienteID_id = iclienteid).activo().annotate(
         estado_registro = F('iClienteID__bEstadoRegistro')
      ).filter(estado_registro =0).annotate(   
         id_sucursal=F('iSucursalID_id'),
         nombre_sucursal =F('iSucursalID__vcNombre'), 
         id_cliente = F('iClienteID'),
         razon_social = F('iClienteID__vcRazonSocial'),
         nombre_fantasia = F('iClienteID__vcNombreFantasia') if not None else None,
         identificador =F('iClienteID__vcIdentificador')).values('id_cliente', 'razon_social', 'nombre_fantasia', 'identificador','id_sucursal','nombre_sucursal', 'estado_registro')
      return sucursales