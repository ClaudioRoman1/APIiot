from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmFlota.Models.AdmFlotaModel import AdmFlota
from Apps.Administracion.AdmSolicitud.Querysets.AdmSolicitudQueryset import AdmSolicitudQuerySet
from Apps.Administracion.AdmUsuarioVehiculo.Models.AdmUsuarioVehiculoModel import AdmUsuarioVehiculo
from Apps.Administracion.AdmVehiculoDispositivo.Models.AdmVehiculoDispositivoModel import AdmVehiculoDispositivo
from Apps.RestBase.Constantes import estadoDispositivo
from Apps.RestBase.RestBaseModel import RestBase


class AdmSolicitud(RestBase):
   iSolicitudID = models.AutoField("Código del registro", primary_key=True)
   iUsuarioVehiculoID = models.ForeignKey(AdmUsuarioVehiculo, on_delete=PROTECT, related_name="AdmSolicitud_AdmUsuarioVehiculo", db_column="iUsuarioVehiculoID")
   iVehiculoDispositivoID = models.ForeignKey(AdmVehiculoDispositivo, on_delete=PROTECT, related_name="AdmSolicitud_AdmVehiculoDispositivo", db_column="iVehiculoDispositivoID")
   jImagenes = models.JSONField()
   bEstado= models.IntegerField(default=1)

   
   
   objects = AdmSolicitudQuerySet.as_manager()

   class Meta:
      db_table = 'ADM_Solicitud'
      managed = False
   
 
   def __str__(self):
      return f' ID del registro: {self.iSolicitudID}'

   def crear(self,datos):
      solicitud = AdmSolicitud.objects.create(
         iUsuarioVehiculoID = datos['id_usuario_vehiculo'],
         iVehiculoDispositivoID =  datos['id_vehiculo_dispositivo'] ,
         jImagenes = datos['imagenes'] if 'imagenes' in datos else None,
         iUsuarioCreacionID = datos['id_usuario_sesion'],
         dtmCreacion = datos['fecha_proceso'],
         bEstado = 1,
         bActivo=1,
      )
      return solicitud
   
   def editar(instancia , datos):
      return instancia
   
   def cambiar_estado(self,datos):
      self.bEstado = datos['estado']
      self.iUsuarioUltimaModificacionID = datos['id_usuario_sesion']
      self.dtmUltimaModificacion = datos['fecha_proceso']
      self.save(update_fields=['bEstado', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])
      return self