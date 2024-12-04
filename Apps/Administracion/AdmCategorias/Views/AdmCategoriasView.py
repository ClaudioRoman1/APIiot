
from rest_framework.response import Response 
from rest_framework import status, generics
from django.utils import timezone
from Apps.Administracion.AdmCategorias.Serializers.AdmCategoriasSerializer import CrearCategoriaSerializer, DesactivarCategoriaSerializer
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Funciones.Encriptacion import  valida_token
from Funciones.ObjetoRetorno import retorno
from django.db import transaction
from Apps.Administracion.AdmCategorias.Models.AdmCategoriasModel import AdmCategorias
from Apps.RestBase.Constantes import  MensajeRetornos
from Funciones.Validaciones import valida_perfil_admin


class CrearCategoriaView (generics.CreateAPIView):

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
		descripcion_categoria = request.data.get('descripcion_categoria')
		nombre_categoria = request.data.get('nombre_categoria')
		imagen_url = request.data.get('imagen_url')
		fecha_proceso = timezone.now()
				
		datos = {
		"descripcion_categoria":descripcion_categoria,
		"nombre_categoria":nombre_categoria,
		"imagen_url":imagen_url,
		"id_usuario_sesion":id_usuario_sesion,
		"fecha_proceso": fecha_proceso 
		}
		
		serializador = CrearCategoriaSerializer(data=datos)
		if not serializador.is_valid():
				return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

		with transaction.atomic():
				try:
						AdmCategorias.crear_categoria(self, datos)
						return Response(retorno(status.HTTP_201_CREATED, 1, 'Creación exitosa'))
				except Exception as a:
						return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))


class DesactivarCategoriaView (generics.UpdateAPIView):

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
		id_categoria = request.data.get('id_categoria')
		fecha_proceso = timezone.now()
		datos = {
		"id_usuario_sesion":id_usuario_sesion,
		"id_categoria":id_categoria,
		"fecha_proceso": fecha_proceso
		}
		categoria = AdmCategorias.objects.por_id_activo(categoriaid=id_categoria)
		if not categoria.exists():
			return Response(retorno(status.HTTP_404_NOT_FOUND, 1, MensajeRetornos.mensajeNoExisteCategoria))
			
		serializador = DesactivarCategoriaSerializer(data=datos)
		if not serializador.is_valid():
				return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

		with transaction.atomic():
			try:
					AdmCategorias.desactivar_categoria(categoria.first(), datos)
					return Response(retorno(status.HTTP_200_OK, 1, MensajeRetornos.mensajeCategoriaEliminada))
			except Exception as a:
					return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))

