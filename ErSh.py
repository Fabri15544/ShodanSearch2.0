import shodan
import random
import string
import time
from termcolor import colored
from colorama import init
init()
print("\n")
print("\n")
print("\n")
print(colored("[NO ME HAGO RESPONSABLE DEL MAL USO DE ESTA HERRAMIENTA]","red"))
print(colored("[NO ME HAGO RESPONSABLE DEL MAL USO DE ESTA HERRAMIENTA]","red"))
print(colored("[NO ME HAGO RESPONSABLE DEL MAL USO DE ESTA HERRAMIENTA]","red"))
print(colored("[NO ME HAGO RESPONSABLE DEL MAL USO DE ESTA HERRAMIENTA]","red"))
print(colored("[NO ME HAGO RESPONSABLE DEL MAL USO DE ESTA HERRAMIENTA]","red"))
print("\n")
print("\n")
print("-----------------------------")
print(colored("BUSQUEDA ERRATICA EN SHODAN","white"))
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
max_range = int(input(colored("Enter the maximum number of characters to generate (Recommended 1 al 4, default = 4)): ","cyan"))or 4)

# Tiempo De Espera
delay = int(input(colored("Enter the delay time between requests (Recommended 1 al 3, default = 1): ","cyan")) or 1)

# Inicia La Busqueda
print(colored("Algo que puede buscar(OpenSSH,Microsoft,nginx,Apache,Windows,Remote,","green"))
print(colored("lwIP,Desktop,DNVRS,usuario,web,webs,webserver,VNC,RTSP,view camera,JPG","green"))
print(colored("Puede usar el valor - para indicar que no se busque algon en SHODAN","green"))
print(colored("No Es Obligatorio Poner Algo","yellow") + "\n")
query = input(colored("Buscar: ","cyan"))
print("\n")

# Filtra En La Pagina
print(colored("LOS FILTROS PUEDEN TARDAR EN CARGAR...(Sin Filtro Dejar En Blanco)","yellow"))
print("\n")
name = input(colored("Filtrar Por (Ciudad/Region): ","cyan"))
print("\n")
print(colored("EL NOMBRE DEL SERVICIO DEBE SER IGUAL","yellow"))
print(colored("O NO BUSCARA NADA , SE LE MOSTRARAN ","yellow"))
print(colored("LOS SERVICIOS EN COLOR AMARILLO AL REALIZAR","yellow"))
print(colored("UNA BUSQUEDA","yellow"))
print("\n")
servicio = input(colored("Filtrar Por Servicio: ","cyan"))
print("\n")
html = input(colored("Filtrar Dentro De Cada HTML con una palabra clave: ","cyan"))
print("\n")

# Crea Una lista vacia
results = []
Iterar = True

# Abre El Archivo De Texto Y Escribe En El
if query is not None:
   # Genera Caracteres Aleatorios
   numeros = "0123456789"
   random_save = "".join(random.choices(numeros, k=64))
   with open(random_save + ".txt", "w", encoding="utf-8") as f:
    # Inicia El Bucle
    while True:
            # Genera Caracteres Aleatorios
            max_chars = random.randint(1, max_range)
            characters = [" ABCDEFGHIJKLMNOPQRSTUVWXYZ "," abcdefghijklmnopqrstuvwxyz "," 0123456789 "]
            random_query = ("".join(random.choices(characters[0], k=max_chars)),"".join(random.choices(characters[1], k=max_chars)),"".join(random.choices(characters[2], k=max_chars)),"".join(random.choices(characters[0]+characters[1], k=max_chars)),"".join(random.choices(characters[0]+characters[1]+characters[2], k=max_chars)))
            
            random_string = '"' + random.choice(random_query) + '"'
            busqueda = query + " " + random_string
            
            # Busca En Shodan
            search_results = api.search(busqueda)
            
            if search_results["total"] > 0:
                # Filtra En La Busqueda Si Hay Filtro
                for result in search_results["matches"]:
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
                                 print(f"Resultados De La Busqueda: {ip}:{port} ({os}) {region}, {city}" + " " + colored("SERVICIO: ","cyan") + colored(services,"yellow"))
                                 f.write(f"{ip},{port},{os},{region},{city},{services}\n")
            print(colored("No Encontre Coincidencias Con: ","red") + colored(busqueda,"cyan"),"\r" * 20, end="")
            
            # Tiempo Espera Busqueda
            time.sleep(delay)
