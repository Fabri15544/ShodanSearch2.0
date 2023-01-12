import shodan
import random
import string
import time

print("-----------------------------")
print("BUSQUEDA ERRATICA EN SHODAN")
print("-----------------------------")
print("\n")


# Trata de leer la clave de API del archivo "api_key.txt"
try:
    with open("api_key.txt", "r") as f:
        api_key = f.read()
# Si el archivo no existe, pide al usuario que ingrese la clave de API y la guarda en el archivo
except FileNotFoundError:
    api_key = input("Ingresa tu clave de API de Shodan: ")
    with open("api_key.txt", "w") as f:
        f.write(api_key)
        
# inicia la api
api = shodan.Shodan(api_key)

# Maximo De Letras A Generar
max_chars = int(input("Numero Maximo De Letras (Recomendado de 1 al 4): "))
print("\n")

# Tiempo De Espera
delay = int(input("Tiempo Espera Entre Solicitudes (Recomendado de 8 a 15): "))
print("\n")

# Muestra una lista ISP Cargado Desde Shodan
#results = api.search(query='isp')

# Muestra los resultados
#for result in results['matches']:
#    print(result['isp'])

# Inicia La Busqueda
print("Filtro: ISP/PAIS/MODELO/EXTENCION EJ:JPG , view camera")
print("Se Puede Usar El - Para indicar que no muestre algo(Ej: -OpenSSH -Microsoft -nginx -Apache -Windows -Remote -lwIP -Desktop -DNVRS -usuario  -web -webs -webserver -VNC -RTSP)")
print("ISP AR: Telecom Argentina S.A")
print("No Es Obligatorio Poner Algo")
query = input("Buscar: ")
print("\n")

# Filtra En La Pagina
print("LOS FILTROS PUEDEN TARDAR EN CARGAR...(Sin Filtro Dejar En Blanco)" + "\n")
print("Para Filtrar Los resultados Buscados Por (Ciudad/Region)")
name = input("Filtrar Resultados Busqueda: ")
print("\n")
print("ES OBLIGATORIO PONER EL SERVICIO DE LO CONTRARIO BUSCARA DE FORMA ERRATICA")
servicio = input("Filtrar Por Servicio: ")
print("\n")
html = input("Filtrar Resultados Busqueda Dentro De Cada URL: ")
print("\n")

# Crea Una lista vacia
results = []

# Abre El Archivo De Texto Y Escribe En El
if query is not None:
   # Genera Caracteres Aleatorios
   numeros = "0123456789"
   random_save = "".join(random.choices(numeros, k=64))
   with open(random_save + ".txt", "w", encoding="utf-8") as f:
    # Inicia El Bucle
    while True:
            # Genera Caracteres Aleatorios
            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            random_query = "".join(random.choices(characters, k=max_chars))
            
            # Busca En Shodan
            search_results = api.search(query +" "+ random_query)
            
            # Filtra En La Busqueda Si Hay Filtro
            for result in search_results["matches"]:
               # if 'country_code' in result['location'] or 'city' in result['location'] or 'product' in result["matches"]:
                   if (servicio in result.get('product', [])) and (name in result['location'].get('country_code', []) or name in result['location'].get('city', [])):
                       if html in result['data']:
                         ip = result["ip_str"]
                         port = result["port"]
                         os = result["os"]
                         if 'product' in result:
                              services = result['product']
                         else:
                              services = None
                         region = result["location"]["country_code"]
                         city = result["location"]["city"]
                    
                              # Guarda Los Datos Sin Repetirlos
                         if ip not in [x[0] for x in results]:
                                 results.append((ip, port, os, region, city, services))
                                 print(f"Resultados De La Busqueda: {ip}:{port} ({os}) ({region}, {city}) ({services})")
                                 f.write(f"{ip},{port},{os},{region},{city},{services}\n")
            
                                 # Tiempo Espera Busqueda
                                 time.sleep(delay)
