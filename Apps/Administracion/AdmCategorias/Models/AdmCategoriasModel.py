from django.db import models
from django.db.models.deletion import PROTECT
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmCategorias.Querysets.AdmCategoriasQueryset import AdmCategoriasQueryset


class AdmCategorias(RestBase):
	CategoriaID = models.AutoField("Código del registro", primary_key=True)
	vcNombre = models.CharField(max_length=80)
	vcDescripcion = models.CharField(null=True, max_length=400)
	ImagenURL = models.CharField(null=True, max_length=200)
	
	objects = AdmCategoriasQueryset.as_manager()

	class Meta:
		db_table = 'adm_categorias'
		managed = False

	def __str__(self):
		return f' ID del registro: {self.CategoriaID}'
	
	def crear_categoria(self, datos):
		AdmCategorias.objects.create(
		vcNombre=datos['nombre_categoria'],
		vcDescripcion=['descripcion_categoria'],
		ImagenURL=['imagen_url'],
		iUsuarioCreacionID=datos['id_usuario_sesion'],
		dtmCreacion=datos['fecha_proceso'],
		bActivo=1
)

	def desactivar_categoria(self, datos):
		self.bActivo = 0
		self.iUsuarioAnulacionID = datos['id_usuario_sesion']
		self.dtmAnulacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioAnulacionID', 'dtmAnulacion'])

	def activar_categoria(self, datos):
		self.bActivo = 1
		self.iUsuarioUltimaModificacionID = datos['id_usuario_sesion']
		self.dtmUltimaModificacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])

