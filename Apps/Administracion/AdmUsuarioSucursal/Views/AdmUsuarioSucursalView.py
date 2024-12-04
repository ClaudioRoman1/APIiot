
from rest_framework.response import Response 
from rest_framework import status, generics
from django.utils import timezone
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.Administracion.AdmUsuarioSucursal.Serializers.AdmUsuarioSucursalSerializer import AsignarUsuarioSucursalViewSerializer
from Apps.RestBase.Constantes import  MensajeRetornos
from Funciones.Encriptacion import  valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction
from Apps.Administracion.AdmUsuarioSucursal.Models.AdmUsuarioSucursalModel import AdmUsuarioSucursal
from Funciones.Validaciones import valida_perfil_admin


class AsignarUsuarioSucursalView (generics.CreateAPIView):

	def post(self, request):
	# Region Validaciones
		valida_jwt = valida_token(request)
		if valida_jwt['mensaje'] != 'valido':
				return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
		id_usuario_sesion = valida_jwt['usuario_id']
		es_admin = valida_perfil_admin(valida_jwt)
		if not es_admin: 
				return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, MensajeRetornos.mensajeNoEsAdmin))
# endRegion
		id_usuario = request.data.get('id_usuario')
		id_sucursal = request.data.get('id_sucursal')
		es_admin = request.data.get('es_admin')
		fecha_proceso = timezone.now()
				
		datos = {
		"id_usuario":id_usuario,
		"id_sucursal":id_sucursal,
		"es_admin":es_admin,
		"id_usuario_sesion":id_usuario_sesion,
		"fecha_proceso": fecha_proceso 
		}
		
		serializador = AsignarUsuarioSucursalViewSerializer(data=datos)
		if not serializador.is_valid():
				return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

		with transaction.atomic():
				try:
						AdmUsuarioSucursal.crear_usuario_sucursal(self, datos)
						return Response(retorno(status.HTTP_201_CREATED, 1, 'Creación exitosa'))
				except Exception as a:
						return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))
