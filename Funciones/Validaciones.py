        

from datetime import datetime
import os
import random
from Apps.Administracion.AdmUsuario.Models.AdmUsuarioModel import AdmUsuario
from Apps.Administracion.AdmUsuarioClientePerfil.Models.AdmUsuarioClientePerfilModel import AdmUsuarioClientePerfil
from Apps.RestBase.Constantes import  constantesList

from barcode import generate
from barcode.writer import ImageWriter
from PIL import Image
from io import BytesIO

# Generar un código UPC aleatorio
        
def valida_perfil_admin(datos_token):
    id_cliente_usuario = datos_token['id_cliente_usuario'][0]
    perfiles = AdmUsuarioClientePerfil.objects.por_cliente_usuario(id_cliente_usuario).activo()
    for perfil  in  perfiles :
        if  perfil.iPerfilID_id in constantesList.usuarioAdministrador:
            return True
    return False

# def valida_perfil_encargado_bodega_o_admin(datos_token) :
#     id_cliente_usuario = datos_token['id_cliente_usuario'][0]
#     perfiles = AdmUsuarioClientePerfil.objects.por_cliente_usuario(id_cliente_usuario).activo()
#     for perfil  in  perfiles :
#         if  perfil.iPerfilID_id in constantesList.usuarioAdministradorOrEncargadoBodega:
#             return True
#     return False

def valida_perfil_admin_cliente(datos_token):
    """Valida el perfil de administrador de un cliente

    Args:
        datos_token (_type_): _description_

    Returns:
        _type_: _description_
    """
    id_cliente_usuario = datos_token['id_cliente_usuario']
    perfiles = AdmUsuarioClientePerfil.objects.por_cliente_usuario(id_cliente_usuario).activo()
    for perfil  in  perfiles :
        if  perfil.iPerfilID_id == constantesList.usuarioAdminCliente :
            return True
    return False
        
# def crear_codigo_producto():
#     numero_aleatorio = ''.join(random.choice('0123456789') for _ in range(12))
#     print(numero_aleatorio)
#     return numero_aleatorio


# def generar_codigo_de_barras(codigo_producto, id_sucursal_cliente):
#         carpeta_codigos_barras = "codigos_de_barras_" + str(id_sucursal_cliente) + '/'
#         if not os.path.exists(carpeta_codigos_barras):
#             os.makedirs(carpeta_codigos_barras)
#         # Genera el código de barras
#         codigo = generate('ean13', codigo_producto,output= (carpeta_codigos_barras  + str("codigo"+codigo_producto)), writer=ImageWriter())
        
#         # Guarda la imagen del código de barras en un archivo en la ruta especificada
#         # Asegúrate de que la carpeta exista, si no, créala
       

#         ruta_imagen = os.path.join( carpeta_codigos_barras,f"{codigo_producto}.png")
        
        
def formatea_fecha(fecha_str):
    fecha = datetime.strptime(fecha_str, '%Y/%m/%d')
    fecha_formateada = fecha.strftime('%Y-%m-%d')
    return fecha_formateada


def transforma_errores_serializador(errores):
        for key, value in errores.items():
            if key == 'non_field_errors':
                if isinstance(value, list) and value:
                    error_message = value[0]
                return error_message
            return errores

    