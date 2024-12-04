from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmSucursal.Models.AdmSucursalModel import AdmSucursal 
from Apps.RestBase.RestBaseModel import RestBase
from Apps.Administracion.AdmUsuarioSucursal.Querysets.AdmUsuarioSucursalQueryset import AdmUsuarioSucursalQueryset
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario


class AdmUsuarioSucursal(RestBase):
	iUsuarioSucursalID = models.AutoField("Código del registro", primary_key=True)
	iSucursalID = models.ForeignKey(AdmSucursal, on_delete=PROTECT, related_name="AdmUsuarioSucursal_AdmSucursal", db_column="iSucursalID")
	iUsuarioID = models.ForeignKey(AdmUsuario, on_delete=PROTECT, related_name="AdmUsuarioSucursal_AdmUsuario", db_column="iUsuarioID")
	esAdmin = models.PositiveSmallIntegerField()
	
	objects = AdmUsuarioSucursalQueryset.as_manager()

	class Meta:
		db_table = 'adm_usuariosucursal'
		managed = False

	def __str__(self):
		return f' ID del registro: {self.iUsuarioSucursalID}'

	def crear_usuario_sucursal(self, datos):
		AdmUsuarioSucursal.objects.create(
			iSucursalID=datos['id_sucursal'],
			iUsuarioID=datos['id_usuario'],
			iUsuarioCreacionID=datos['id_usuario_sesion'],
			esAdmin=datos['es_admin'],
			bActivo=1
		)
