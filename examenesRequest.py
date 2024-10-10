import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os


# Download file functino
def download_file(url, destination_folder):
    print(url)
    try:
        # Realizar la descarga
        response = requests.get(url, stream=True)
        
        # Verificar que la solicitud fue exitosa
        if response.status_code == 200:
            # Obtener el nombre del archivo
            parsed_url = urlparse(url)  # Analiza la URL
            filename = os.path.basename(parsed_url.path)  # Obtiene el nombre base del archivo
            filename = filename.split('?')[0]  # Elimina los parámetros de consulta
            full_path = os.path.join(destination_folder, filename)
            
            # Guardar el contenido del archivo
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Archivo guardado como: {full_path}")
        else:
            print(f"Error al descargar el archivo desde {url}: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error al descargar el archivo: {e}")





# URL de la página de inicio de sesión
url_login = 'https://ris.clinicaloscarrera.cl/RISWEB/Timeout.aspx'

# Credentials
credentials = {
    'username': 'Jmoreno',
    'password': 'jm.clc2018'
}

# Start a session so that cookies are retained
session = requests.Session()

# Send a POST request to the login URL with the payload
credentials_resp = session.post(url_login, data=credentials)

"""
if credentials_resp.status_code == 200:
    print(":D")

else:
    print("D:")
"""

# Almacenar respuesta de URL
protected_page = 'https://ris.clinicaloscarrera.cl/RISWEB/Web/Examen/ListaExamen.aspx'
resp = session.get(protected_page)



if resp.status_code == 200:
    print('inicio')
    soup = BeautifulSoup(resp.text, 'html.parser')
    Users_complete = soup.find_all('tr', class_=['rowlist', 'alternaterowlist'])
    i = 0
    for Users in Users_complete:
        #print(Users)
        
        # Filter and Search all <a> tags with an href that redirects to another page or resource (that means it has a button to download 4 example)
        user_download_options = Users.find_all('a', href = True)
        #print(user_download_options)
        

        # Crear una carpeta de descargas en el directorio del usuario
        user_home = os.path.expanduser("~")  
        download_folder = os.path.join(user_home, 'Descargas', 'Examenes')  # Create Folder

        # Crear la carpeta si no existe
        os.makedirs(download_folder, exist_ok=True)     

        for option in user_download_options:
            if option.get('title') == 'Descargar Examen':
                i += 1
                #print(i, '---------------------', option.get('href'))
                download_file(option.get('href'), download_folder)    
else: 
    print("Error to make petition", resp.status_code)


session.close()