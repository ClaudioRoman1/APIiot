from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models.deletion import PROTECT
from Apps.Administracion.AdmPais.Models.AdmPaisModel import AdmPais
from Apps.RestBase.RestBaseModel import RestBase

from Apps.Administracion.AdmUsuario.Querysets.AdmUsuarioQuerysets import AdmUsuarioQueryset


class AdmUsuario(RestBase):
	iUsuarioID = models.AutoField("Código del registro", primary_key=True)
	vcNombre = models.CharField(max_length=100)
	vcApellidos = models.CharField(max_length=100)
	vcIdentificador = models.CharField(max_length=40, unique=True)
	vcNumeroMovil = models.CharField(max_length=14)
	vcCorreoElectronico = models.CharField(null=True, max_length=50, unique=True)
	iPaisID = models.ForeignKey(AdmPais, on_delete=PROTECT, related_name="AdmUsuario_AdmPais", db_column="iPaisID")
	vcDireccion = models.CharField(max_length=200)
	vcContrasena = models.CharField(null=True, max_length=50)
	# iDomRol = models.IntegerField(null=True, default=4)
	
	objects = AdmUsuarioQueryset.as_manager()

	class Meta:
		db_table = 'ADM_Usuario'
		managed = False
		
	def crear(self, datos):
		usuario = AdmUsuario.objects.create(
				vcNombre=datos['nombre'],
				vcApellidos=datos['apellidos'],
				vcIdentificador=datos['identificador'],
				vcNumeroMovil=datos['num_cel'],
				vcCorreoElectronico=datos['correo_electronico'],
				iPaisID_id=datos['id_pais'],
				vcContrasena=datos['contraseña'],
				iUsuarioCreacionID=datos['id_usuario_sesion'],
				dtmCreacion=datos['fecha_proceso'],
				bActivo=1)
		return usuario
		
	def eliminacion_logica_usuario(self, datos):
		self.bActivo = 0
		self.iUsuarioAnulacionID = datos['id_usuario']
		self.dtmAnulacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioAnulacionID', 'dtmAnulacion'])

  
	def activar_usuario(self, datos):

		self.bActivo = 1
		self.iUsuarioUltimaModificacionID = datos['id_usuario']
		self.dtmUltimaModificacion = datos['fecha_proceso']
		self.save(update_fields=['bActivo', 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'])  

  
	def editar(self, datos, usuario_id):
		usuario = self.objects.filter(iUsuarioID=usuario_id)

		if usuario.first():
			campos_actualizables = {}

			campos_a_verificar = [
				'vcNombre', 'vcApellidos', 'vcIdentificador', 'vcNumeroMovil',
				'vcCorreoElectronico', 'iPaisID_id', 
				 'vcDireccion', 
				 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion'
			]
		
			for campo in campos_a_verificar:
				if campo in datos and datos[campo] != getattr(usuario.first(), campo) and datos[campo] is not None:
					campos_actualizables[campo] = datos[campo]

			try:
				campos_actualizables['dtmUltimaModificacion'] = datetime.now()
				usuario.update(**campos_actualizables)
				return usuario.first()
			except Exception as e:
				# Manejar errores de actualización de la base de datos
				return 'error-1'

		# Manejar el caso en que el usuario no existe
		return None
	def cambiar_contrasena(self,usuario,datos):
		usuario.iUsuarioUltimaModificacionID = datos['id_usuario']
		usuario.dtmUltimaModificacion = datos['fecha_proceso']
		usuario.vcContrasena = datos['nueva_contrasena']
		usuario.save(update_fields=[ 'iUsuarioUltimaModificacionID', 'dtmUltimaModificacion', 'vcContrasena']) 
		return usuario