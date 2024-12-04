from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmDispositivo.Querysets.AdmDispositivoQueryset import AdmDispositivoQueryset
from Apps.RestBase.Constantes import estadoDispositivo
from Apps.RestBase.RestBaseModel import RestBase


class AdmDispositivo(RestBase):
   iDispositivoID = models.AutoField("Código del registro", primary_key=True)
   iTipoDispositivoID = models.IntegerField(null=False)
   vcCodigo = models.CharField(max_length=80)
   bEstado = models.BooleanField(default=False)
   objects = AdmDispositivoQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Dispositivo'
      managed = False
   def crear(self, datos):
      return self.objects.create(
      iTipoDispositivoID = datos['id_tipo_dispositivo'],
      vcCodigo = datos['codigo'],
      iUsuarioCreacionID = datos['id_usuario_sesion'],
      dtmCreacion = datos['fecha_proceso'],
      bEstado=False,
      bActivo = True
      )
      
   def abrir(self,datos):
      self.bEstado = estadoDispositivo.abierto
      self.iUsuarioUltimaModificacionID = datos['id_usuario_sesion']
      self.dtmUltimaModificacion = datos['fecha_proceso']
      self.save(update_fields=['bEstado', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])
      return self
   
   def cerrar(self,datos):
      self.bEstado = estadoDispositivo.cerrado
      self.iUsuarioUltimaModificacionID = datos['id_usuario_sesion']
      self.dtmUltimaModificacion = datos['fecha_proceso']
      self.save(update_fields=['bEstado', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])
      return self
      