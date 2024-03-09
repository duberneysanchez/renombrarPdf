import os
import re
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import PyPDF2

def reemplazar_caracteres_no_permitidos(cadena):
    """Reemplaza los caracteres no permitidos en el nombre del archivo"""
    caracteres_no_permitidos = r'[^a-zA-Z0-9_\-. ]'
    return re.sub(caracteres_no_permitidos, '_', cadena)

def obtener_numero_cuenta(texto):
    """Obtiene el número de cuenta del texto"""
    patron = r'No\. ([A-Z0-9]+) CÓDIGO : ([0-9-]+)'
    coincidencias = re.search(patron, texto)
    if coincidencias:
        numero_cuenta = coincidencias.group(1) + ' ' + coincidencias.group(2)
        return numero_cuenta.strip()
    return None

# Ruta a tu archivo de credenciales de servicio de Google Drive
ruta_credenciales = 'ruta_a_tu_archivo_de_credenciales.json'

# Crea las credenciales de servicio
gauth = GoogleAuth()
gauth.credentials = service_account.Credentials.from_service_account_file(ruta_credenciales)

# Crea el cliente de Google Drive
drive = GoogleDrive(gauth)

# ID de la carpeta en Google Drive que contiene los certificados
carpeta_id = '1ptel_ZAKckSWe4wM3sj_IgI1v-htal2F'

# Obtén la lista de archivos en la carpeta
lista_archivos = drive.ListFile({'q': f"'{carpeta_id}' in parents and trashed=false"}).GetList()

for archivo in lista_archivos:
    if archivo['mimeType'] == 'application/pdf':
        try:
            # Descarga el archivo PDF y abrelo
            nombre_archivo = archivo['title']
            ruta_archivo_local = os.path.join(os.getcwd(), nombre_archivo)
            archivo.GetContentFile(ruta_archivo_local)
            pdfFileObject = open(ruta_archivo_local, 'rb')

            # Lee el texto del archivo PDF
            pdfReader = PyPDF2.PdfReader(pdfFileObject)
            pageObject = pdfReader.pages[0]
            text = pageObject.extract_text()
            
            # Obtén el número de cuenta
            accountNumber = obtener_numero_cuenta(text)
            if accountNumber:
                accountNumber = reemplazar_caracteres_no_permitidos(accountNumber)
                pdfFileObject.close()

                # Renombra el archivo
                new_name = os.path.join(os.getcwd(), accountNumber + '.pdf')
                if os.path.exists(new_name):
                    print(f'El archivo {new_name} ya existe.')
                else:
                    os.rename(ruta_archivo_local, new_name)
                    print(f'Renombrado {nombre_archivo} a {new_name}')
            else:
                print(f'No se encontró número de cuenta en {nombre_archivo}')
            
            # Elimina el archivo local descargado
            os.remove(ruta_archivo_local)
            
        except Exception as e:
            print(f'Ocurrió un error al procesar {nombre_archivo}: {str(e)}')
