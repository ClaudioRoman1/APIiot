from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
from Apps.Administracion.AdmClienteUsuario.Querysets.AdmClienteUsuarioQueryset import AdmClienteUsuarioQueryset
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.RestBase.RestBaseModel import RestBase



class AdmClienteUsuario(RestBase):
   iClienteUsuarioID = models.AutoField("Código del registro", primary_key=True)
   iClienteID = models.ForeignKey(AdmCliente, on_delete=PROTECT, related_name="ClienteUsuario_Cliente", db_column="iClienteID")
   iUsuarioID = models.ForeignKey(AdmUsuario, on_delete=PROTECT, related_name="ClienteUsuario_Usuario", db_column="iUsuarioID")
   
   objects = AdmClienteUsuarioQueryset.as_manager()

   class Meta:
      db_table = 'ADM_ClienteUsuario'
      managed = False

   def __str__(self):
      return f' ID del registro: {self.iClienteUsuarioID}'
   
   def crear_cliente_usuario(self,datos,usuario,cliente):
      cliente_usuario = AdmClienteUsuario.objects.create(
         iUsuarioID = usuario,
         iClienteID = cliente,
         iUsuarioCreacionID = datos['id_usuario_sesion'],
         dtmCreacion = datos['fecha_proceso'],
      )
      return cliente_usuario

