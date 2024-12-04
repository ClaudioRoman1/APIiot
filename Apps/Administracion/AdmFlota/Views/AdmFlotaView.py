from rest_framework import generics, status
from rest_framework.response import Response
from Apps.Administracion.AdmFlota.Models.AdmFlotaModel import AdmFlota
from Apps.Administracion.AdmFlota.Serializers.AdmFlotaSerializer import ListaFlotaSerializer
from Funciones.ObjetoRetorno import retorno

class  ListaFlotasView(generics.ListAPIView):
    """Metodo que muestra la lista de regiones por países
       Retorno: retorno
       Elaborado por: CRoman 13-05-23
    """
    
    def post(self,request):
        id_cliente = request.data.get('id_cliente')
        datos = {
            'id_cliente':id_cliente
        }
        serializer = ListaFlotaSerializer(data=datos)
        if serializer.is_valid():
            flotas = AdmFlota.objects.por_cliente(iclienteid = id_cliente).activo()
            ls_flotas = list(flotas)
            
            if len(ls_flotas) ==0:
                return Response(retorno(status.HTTP_200_OK, 0, 'No hay flotas ', None,None))
        
            lista_flotas = ListaFlotaSerializer(flotas,many=True)
            lista_flotas_serializadas= lista_flotas.data 
            total_reg = len(lista_flotas_serializadas)
        
        
            return Response(retorno(status.HTTP_200_OK, 1, 'Exitoso',lista_flotas_serializadas, total_reg ))
        


