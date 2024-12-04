from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.Administracion.AdmUsuarioVehiculo.Querysets.AdmUsuarioVehiculoQueryset import AdmUsuarioVehiculoQueryset
from Apps.Administracion.AdmVehiculo.Models.AdmVehiculoModel import AdmVehiculo
from Apps.RestBase.RestBaseModel import RestBase


class AdmUsuarioVehiculo(RestBase):
   iUsuarioVehiculoID = models.AutoField("Código del registro", primary_key=True)
   iVehiculoID = models.ForeignKey(AdmVehiculo, on_delete=PROTECT, related_name="AdmUsuarioVehiculo_AdmVehiculo", db_column="iVehiculoID")
   iUsuarioID = models.ForeignKey(AdmUsuario, on_delete=PROTECT, related_name="AdmUsuarioVehiculo_AdmUsuario", db_column="iUsuarioID")
   
   objects = AdmUsuarioVehiculoQueryset.as_manager()

   class Meta:
      db_table = 'ADM_UsuarioVehiculo'
      managed = False
      
   def asignar(self,datos):
      return self.objects.create(
				iUsuarioID_id=datos['id_usuario'],
				iVehiculoID_id=datos['id_vehiculo'],
				iUsuarioCreacionID=datos['id_usuario_sesion'],
				dtmCreacion=datos['fecha_proceso'],
				bActivo=True)