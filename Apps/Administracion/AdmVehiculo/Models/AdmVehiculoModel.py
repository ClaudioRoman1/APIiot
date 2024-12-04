from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmFlota.Models.AdmFlotaModel import AdmFlota
from Apps.Administracion.AdmVehiculo.Querysets.AdmVehiculoQueryset import AdmVehiculoQueryset
from Apps.RestBase.RestBaseModel import RestBase


class AdmVehiculo(RestBase):
   iVehiculoID = models.AutoField("Código del registro", primary_key=True)
   iFlotaID = models.ForeignKey(AdmFlota, on_delete=PROTECT, related_name="AdmVehiculo_AdmFlota", db_column="iFlotaID")
   vcPatente = models.CharField(max_length=10)
   vcMarca = models.CharField(max_length=40)
   nCantidadTotalLitros= models.DecimalField(decimal_places=2,max_digits=10)
   iAno = models.IntegerField(null=False)
   
   
   objects = AdmVehiculoQueryset.as_manager()

   class Meta:
      db_table = 'ADM_Vehiculo'
      managed = False
   
 
   def __str__(self):
      return f' ID del registro: {self.iVehiculoID}'

   def crear(self,datos):
      vehiculo = AdmVehiculo.objects.create(
         iFlotaID_id = datos['id_flota'],
         vcPatente =  datos['num_patente'] if 'num_patente' in datos   else None,
         vcMarca = datos['marca'] if 'marca' in datos else None,
         iAno = datos['ano'] if 'ano' in datos else None,
         nCantidadTotalLitros= datos['cantidad_litros'] if 'cantidad_litros' in datos else None,
         iUsuarioCreacionID = datos['id_usuario_sesion'],
         dtmCreacion = datos['fecha_proceso'],
         bActivo=1,
      )
      return vehiculo