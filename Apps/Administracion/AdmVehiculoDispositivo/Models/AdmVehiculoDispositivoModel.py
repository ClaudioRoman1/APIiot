from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmDispositivo.Models.AdmDispositivoModel import AdmDispositivo
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.Administracion.AdmVehiculoDispositivo.Querysets.AdmVehiculoDispositivoQueryset import AdmVehiculoDispositivoQueryset
from Apps.RestBase.Constantes import estadosSolicitud
from Apps.RestBase.RestBaseModel import RestBase


class AdmVehiculoDispositivo(RestBase):
   iVehiculoDispositivoID = models.AutoField("Código del registro", primary_key=True)
   iDispositivoID = models.ForeignKey(AdmDispositivo, on_delete=PROTECT, related_name="AdmVehiculoDispositivo_AdmDispositivo", db_column="iDispositivoID")
   iVehiculoID = models.ForeignKey(AdmVehiculo, on_delete=PROTECT, related_name="AdmVehiculoDispositivo_AdmVehiculo", db_column="iVehiculoID")

   
   objects = AdmVehiculoDispositivoQueryset.as_manager()

   class Meta:
      db_table = 'ADM_VehiculoDispositivo'
      managed = False
   
   def crear(self,datos):
      self.objects.create(
		iDispositivoID_id = datos['id_dispositivo'],
		iVehiculoID_id = datos['id_vehiculo'],
		iUsuarioCreacionID = datos['id_usuario_sesion'],
		dtmCreacion = datos['fecha_proceso'],
		bActivo = True)
      
      
   
      