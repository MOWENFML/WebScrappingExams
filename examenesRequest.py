import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# Define el User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Función para descargar archivos
def download_file(url, destination_folder, file_number):
    try:
        # Realizar la descarga
        response = session.get(url, headers=headers, stream=True)  # Incluye el User-Agent en la descarga

        if response.status_code == 200:
            # Nombrar el archivo como Examen1, Examen2, ...
            filename = f"Examen{file_number}.rar"
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

# Credenciales
credentials = {
    'username': 'Jmoreno',
    'password': 'jm.clc2018'
}

# Iniciar una sesión para mantener las cookies
session = requests.Session()

# Enviar la solicitud POST con el User-Agent
credentials_resp = session.post(url_login, data=credentials, headers=headers)

# Verificar si la sesión se inició correctamente
if credentials_resp.status_code == 200:
    print(":D Sesión iniciada correctamente")
else:
    print("D: Error al iniciar sesión")

# URL protegida con los archivos
protected_page = 'https://ris.clinicaloscarrera.cl/RISWEB/Web/Examen/ListaExamen.aspx'
resp = session.get(protected_page, headers=headers)

# Si la página protegida es accesible
if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, 'html.parser')
    users_complete = soup.find_all('tr', class_=['rowlist', 'alternaterowlist'])

    # Crear una carpeta para guardar los exámenes
    download_folder = os.path.join(os.path.expanduser("~"), 'Descargas', 'Examenes')
    os.makedirs(download_folder, exist_ok=True)

    # Descargar los archivos
    file_number = 1
    for user in users_complete:
        user_download_options = user.find_all('a', href=True)
        
        for option in user_download_options:
            if option.get('title') == 'Descargar Examen':
                download_url = option.get('href')  # Obtener el enlace de descarga
                download_file(download_url, download_folder, file_number)
                file_number += 1
else:
    print("Error al acceder a la página protegida:", resp.status_code)

session.close()
