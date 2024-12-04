
# from rest_framework.response import Response 
# from rest_framework import status, generics
# from django.utils import timezone
# from Apps.Administracion.AdmCliente.Models.AdmClienteModel import AdmCliente
# from Apps.Administracion.AdmCliente.Serializers.AdmClienteSerializer import CrearClienteSerializer
# from Apps.RestBase.Constantes import MensajeRetornos
# from Funciones.Encriptacion import  valida_token
# from Funciones.ObjetoRetorno import retorno
# from django.db import transaction


    
# class CrearClienteView (generics.CreateAPIView):
#     # Funcion para crear cliente
#     def post(self, request):
#         valida_jwt = valida_token(request)
#         if valida_jwt['mensaje'] != 'valido':
#             return Response(retorno(status.HTTP_401_UNAUTHORIZED, 0, valida_jwt['mensaje'], 1))
#         id_usuario = valida_jwt['usuario_id']
#         razonSocial = request.data.get('razonSocial')
#         nombreFantasia = request.data.get('nombreFantasia')
#         identificador = request.data.get('identificador')
#         fecha_proceso = timezone.now()
    
#         datos = {
#         "id_usuario":id_usuario,
#         "razonSocial":razonSocial,
#         "identificador":identificador,
#         "nombreFantasia":nombreFantasia,
#         "fecha_proceso": fecha_proceso 
#         }
        
#         serializador = CrearClienteSerializer(data=datos)
#         if not serializador.is_valid():
#             return Response(retorno(status.HTTP_400_BAD_REQUEST, 0, serializador.errors, ''))

#         with transaction.atomic():
#             try:
#                 AdmCliente.crear(self,datos)
#                 return Response(retorno(status.HTTP_201_CREATED, 1,MensajeRetornos.mensajeCreacionOk))
#             except Exception as a:
#                 return Response(retorno(status.HTTP_400_BAD_REQUEST, 1, 'ERROR: ' + str(a)))
    
            