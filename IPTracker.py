# Este programa permite consultar la ip y saber su ubicacion al igual que los puertos abiertos
# Identifica los puertos abiertos

import socket
import requests
from os import system
import os
import datetime

if not os.path.exists('reports'):
    os.makedirs('reports')

# Obtener la clave de API de VirusTotal
# Se debera crear una cuenta en VirusTotal para obtener la API
api_key = 'API_KEY_HERE'

# Verificar si la dirección IP es maliciosa utilizando la API de VirusTotal
def is_malicious(ip, api_key):
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip}'
    headers = {'x-apikey': api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        stats = data.get('attributes', {}).get('last_analysis_stats', {})
        if stats.get('malicious') or stats.get('suspicious'):
            return True
    return False

# Función para determinar la clase de la dirección IP
def get_ip_class(ip):
    octeto = int(ip.split(".")[0])
    if octeto <= 127:
        return "A"
    elif octeto <= 191:
        return "B"
    elif octeto <= 223:
        return "C"
    else:
        return "No es una dirección de clase A, B o C"

# Función para escanear los puertos de una dirección IP
def scan_ports(ip):
    print(f"\nEscaneando puertos en {ip}...")
    for port in range(1, 65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Puerto {port} abierto")
        sock.close()
system('cls')

# Menu
print("Bienvenido, por favor seleccione una opción:")
print("1. Ingresar URL")
print("2. Consultar mi dirección IP")
print("3. Escanear puertos en una dirección IP")
print("4. Salir")
opcion = input("Opción: ")

if opcion == "1":
    # Solicitar la URL al usuario
    site = input("\nIngrese la URL: ")
    ip = socket.gethostbyname(site)
    # Verificar si la dirección IP es maliciosa
    if is_malicious(ip, api_key):
        print('La dirección IP ha sido reportada como maliciosa')
    else:
        print('La dirección IP no ha sido reportada como maliciosa')
elif opcion == "2":
    # Obtener la dirección IP de este equipo
    ip = requests.get('https://api.ipify.org').text
    # Verificar si la dirección IP es maliciosa
    if is_malicious(ip, api_key):
        print('La dirección IP ha sido reportada como maliciosa')
    else:
        print('La dirección IP no ha sido reportada como maliciosa')
elif opcion == "3":
    # Solicitar la dirección IP al usuario
    ip = input("\nIngrese la dirección IP a escanear: ")
    scan_ports(ip)
    exit()
elif opcion == "4":
    # Salir
    exit()
else:
    print("Opción no válida")
    exit()

# Obtener los datos de la dirección IP
got = requests.get(f"http://ip-api.com/json/{ip}").json()
lat = requests.get(f"http://ipwho.is/{ip}").json()

datos = {
    "Dirección IP": got["query"],
    "ISP": got["isp"],
    "Tipo": lat["type"],
    "País": got["country"],
    "Región": got["regionName"],
    "Ciudad": got["city"],
    "Latitud": got["lat"],
    "Longitud": got["lon"],
    "Continente": lat["continent"],
    "Código Postal": lat["postal"],
    "Código de Área": lat["calling_code"],
    "Límites": lat["borders"],
    "Conexión": lat["connection"],
    "Zona Horaria": lat["timezone"],
    "Clase de IP": get_ip_class(ip)
}

# Sue muestran los datos en pantalla
for etiqueta, valor in datos.items():
    print(f"{etiqueta}: {valor}")

# Se escribe un archivo de texto con los resultados
with open('reports/resultados.txt', 'w') as f:
    # Escribir los datos en el archivo .txt
    for etiqueta, valor in datos.items():
        f.write(f"{etiqueta}: {valor}\n")
    # Escribir los puertos abiertos en el archivo si se seleccionó la opción 3
    if opcion == "3":
        f.write(f"\nPuertos abiertos en {ip}:\n")
        for port in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                f.write(f"Puerto {port} abierto\n")
            sock.close()
print(f"\nLos resultados han sido guardados en reports/resultados.txt")
