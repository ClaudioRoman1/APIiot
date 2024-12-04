from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion import AdmUsuario
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmCliente.Querysets.AdmClienteQueryset import AdmClienteQueryset


class AdmCliente(RestBase):
   ClienteID = models.AutoField("Código del registro", primary_key=True)
   vcRazonSocial = models.CharField(null=True, max_length=70)
   vcNombreFantasia = models.CharField(null=True, max_length=70)
   vcIdentificador = models.CharField(null=True, max_length=70)
   bEstadoRegistro = models.IntegerField(null=False, default=0)
   
   objects = AdmClienteQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Cliente'
      managed = False

   def __str__(self):
      return f' ID del registro: {self.ClienteID}'
   
   def crear(self,datos):
      cliente = AdmCliente.objects.create(
         vcRazonSocial = datos['razon_social'],
         vcNombreFantasia =  datos['nombre_fantasia'] if 'nombre_fantasia' in datos   else None,
         vcIdentificador = datos['identificador'],
         iUsuarioCreacionID = datos['id_usuario_sesion'],
         dtmCreacion = datos['fecha_proceso'],
         # bActivo=1,
         bEstadoRegistro = 0
      )
      return cliente

