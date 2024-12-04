
from django.db import models
from django.db.models import When , Case, F
from django.forms import IntegerField

from Apps.RestBase.Constantes import estadoDispositivo, estadosSolicitud 

class AdmSolicitudQuerySet(models.QuerySet):
   def activo(self):
      return self.filter(bActivo = True)

   def por_id(self, isolicitudid):
      return self.filter(iSolicitudID = isolicitudid)
   
   def por_flota(self,iflotaid):
      return self.filter(iFlotaID = iflotaid)
   
   def por_cliente (self, iclienteid ):
      return self.filter(iFlotaID_iClienteID=iclienteid)
   
   def por_patente(self, patente):
      return self.filter(vcPatente = patente)
   
   def por_usuariovehiculo(self, iusuariovehiculoid):
      return self.filter(iUsuarioVehiculoID = iusuariovehiculoid)
   
   def por_vehiculodispositivo(self , ivehiculodispositivoid):
      return self.filter(iVehiculoDispositivoID = ivehiculodispositivoid)
   
   def pendiente(self):
      return self.filter(bEstado=estadosSolicitud.pendiente)
   
   def aceptada(self):
      return self.filter(bEstado=estadosSolicitud.aceptada)
   def rechazada(self):
      return self.filter(bEstado=estadosSolicitud.rechazada)
   
   def por_usuariovehiculo_por_vehiculodispositivo_pendiente(self ,iusuariovehiculoid, ivehiculodispositivoid):
      resultado =self.pendiente().por_usuariovehiculo(iusuariovehiculoid=iusuariovehiculoid).por_vehiculodispositivo(ivehiculodispositivoid = ivehiculodispositivoid)
      return resultado
   def por_usuariovehiculo_por_vehiculodispositivo(self ,iusuariovehiculoid, ivehiculodispositivoid):
      resultado =self.por_usuariovehiculo(iusuariovehiculoid=iusuariovehiculoid).por_vehiculodispositivo(ivehiculodispositivoid = ivehiculodispositivoid)\
   .annotate(
    has_images=Case(
        When(jImagenes__isnull=False, then=1),  # Cuando jImagenes no es null
        When(jImagenes__exact='{}', then=0),    # Cuando jImagenes es un objeto vacío
        default=0,
    )
).order_by('-has_images', '-dtmCreacion', '-dtmUltimaModificacion', '-dtmAnulacion')
      return resultado
   
   def pendientes_annotate(self):
      vehiculo = id_vehiculo_dispositivo= F('iVehiculoDispositivoID__iVehiculoID'),
      return self.filter(bEstado=estadosSolicitud.pendiente).annotate(
         id_solicitud= F('iSolicitudID'),
         id_vehiculo_dispositivo= F('iVehiculoDispositivoID__iVehiculoID_id'),
         ).values('id_solicitud','id_vehiculo_dispositivo')
   
   
