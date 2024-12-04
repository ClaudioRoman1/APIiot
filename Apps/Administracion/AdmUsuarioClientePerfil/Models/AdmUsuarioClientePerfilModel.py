from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmClienteUsuario.Models.AdmClienteUsuarioModel import AdmClienteUsuario
from Apps.Administracion.AdmPerfiles.Models.AdmPerfilesModel import AdmPerfiles
from Apps.Administracion.AdmUsuarioClientePerfil.Querysets.AdmUsuarioClientePerfilQuerysets import AdmUsuarioClientePerfilQueryset
from Apps.RestBase.RestBaseModel import RestBase



class AdmUsuarioClientePerfil(RestBase):
	iUsuarioClientePerfilID = models.AutoField("Código del registro", primary_key=True)
	iClienteUsuarioID = models.ForeignKey(AdmClienteUsuario, on_delete=PROTECT, related_name="AdmUsuarioClientePerfil_AdmClienteUsuario", db_column="iClienteUsuarioID")
	iPerfilID = models.ForeignKey(AdmPerfiles, on_delete=PROTECT, related_name="AdmUsuarioClientePerfil_AdmPerfil", db_column="iPerfilID")

	
	objects = AdmUsuarioClientePerfilQueryset.as_manager()

	class Meta:
		db_table = 'ADM_UsuarioClientePerfil'
		managed = False
		
	def crear(self, datos):
		AdmUsuarioClientePerfil.objects.create(
			iClienteUsuarioID_id=datos['id_usuario_cliente'],
			iPerfilID_id=datos['id_perfil'],
			iUsuarioCreacionID=datos['id_usuario_sesion'],
			dtmCreacion=datos['fecha_proceso'],
			bActivo=1
		)
		
	def desactivar_perfil_cliente_usuario(self, datos):
		self.bActivo = 0
		self.iUsuarioAnulacionID = datos['id_usuario_sesion']
		self.dtmAnulacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioAnulacionID', 'dtmAnulacion'])

  
	def activar_perfil_cliente_usuario(self, datos):
		self.bActivo = 1
		self.iUsuarioUltimaModificacionID = datos['id_usuario']
		self.dtmUltimaModificacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])  

