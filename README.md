# Proyecto-Base
Api Base para desarrollo de cualquier aplicacion web
# Estructura de proyecto
Base
 -- En esta carpeta están todos los archivos de configuración y urls principales del proyecto

Apps
 --Dentro de el están todas las Aplicaciones del proyecto dependiendo del módulo

Funciones
-- Dentro de el estáran todos los archivos con funciones genéricas para el proyecto

# Nomenclatura y composición de endpoints 
La nomenclatura a utilizar para los endpoints será snake case :
    --Ejemplos : 
        -- lista_paises
        -- obtiene_datos
        -- crea_usuarios 
        -- inicia_sesion_usuario
        -- cliente_pais
    
El primer segmento tendrá el nombre en plural de la carpeta sin el 'Adm' del archivo url 
 -- Ejemplo:
    --path('ciudades/', include('Apps.Administracion.AdmCiudad.urls'))  
        -- La carpeta contenedora de esta url es AdmCiudad por lo que el primer segmento del endpoint es ciudades en plural.

El segundo segmento debe ser declarativo de la funcionalidad del servicio (la acción que realiza el servicio)
    --Ejemplo:
        --path('lista_ciudades',ListaCiudadesView.as_view(),name ='Metodo que lista ciudades')



# Ejecutar docker para crear imagen
    -- docker build -t mi_app_django .
# backup DB
pg_dump -h localhost -p 5432 -U postgres -F c -b -v -f "mibase.sql" cerraduras 

# backup DB Restore
C:\Program Files\PostgreSQL\17\bin>pg_restore -h bfkq6iflyubmoqcw5rav-postgresql.services.clever-cloud.com -p 7170 -U uizxlwowfw8didhrqxuj -d bfkq6iflyubmoqcw5rav --format=c mibase.sql
