from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmPais.Models.AdmPaisModel import AdmPais
from Apps.Administracion.AdmPerfiles.Querysets.AdmPerfilesQuerysets import AdmPerfilesQueryset
from Apps.Administracion.AdmRegion.Models.AdmRegionModel import AdmRegion
from Apps.RestBase.RestBaseModel import RestBase



class AdmPerfiles(RestBase):
	iPerfilID = models.AutoField("Código del registro", primary_key=True)
	vcNombre = models.CharField(max_length=100)
	vcDescripcion = models.TextField()

	
	objects = AdmPerfilesQueryset.as_manager()

	class Meta:
		db_table = 'ADM_Perfil'
		managed = False
		
	def crear(self, datos):
		return AdmPerfiles.objects.create(
			vcNombre=datos['nombre'],
			vcDescripcion = datos['descripcion'],
			iUsuarioCreacionID=datos['id_usuario_sesion'],
			dtmCreacion=datos['fecha_proceso'],
			bActivo=1
		)
		
	def desactivar_perfil(self, datos):
		self.bActivo = 0
		self.iUsuarioAnulacionID = datos['id_usuario_sesion']
		self.dtmAnulacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioAnulacionID', 'dtmAnulacion'])

  
	def activar_perfil(self, datos):
		self.bActivo = 1
		self.iUsuarioUltimaModificacionID = datos['id_usuario_sesion']
		self.dtmUltimaModificacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])  
