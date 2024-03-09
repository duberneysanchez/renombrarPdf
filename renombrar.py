import re

def obtener_codigo(texto):
    """Obtiene el código después de 'Fwd:' del texto"""
    patron = r'Asunto: (\w+-\d+-\d+)'
    coincidencias = re.search(patron, texto)
    if coincidencias:
        codigo = coincidencias.group(1)
        return codigo.strip()
    return None


import os
from tkinter import filedialog
import PyPDF2
import re

def reemplazar_caracteres_no_permitidos(cadena):
    """Reemplaza los caracteres no permitidos en el nombre del archivo"""
    caracteres_no_permitidos = r'[^a-zA-Z0-9_\-. ]'
    return re.sub(caracteres_no_permitidos, '_', cadena)

root = filedialog.Tk()
root.directory = filedialog.askdirectory()
route = root.directory+'/'

certificados = [file for file in os.listdir(route) if file.endswith('.pdf')]

for certificado in certificados:
    try:
        pdfFileObject = open(route + certificado, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObject)
        pageObject = pdfReader.pages[0]
        text = pageObject.extract_text()
        accountNumber = obtener_codigo(text)
        if accountNumber:
            accountNumber = reemplazar_caracteres_no_permitidos(accountNumber)
            pdfFileObject.close()

            new_name = route + accountNumber + '.pdf'
            if os.path.exists(new_name):
                print(f'El archivo {new_name} ya existe.')
            else:
                os.rename(route + certificado, new_name)
                print(f'Renombrado {certificado} a {new_name}')
        else:
            print(f'No se encontró número de cuenta en {certificado}')
    except Exception as e:
        print(f'Ocurrió un error al procesar {certificado}: {str(e)}')

