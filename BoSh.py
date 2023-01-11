import shodan
import ipaddress
from termcolor import colored
from colorama import init
init()

print("-----------------------------")
print("BUSCADOR SHODAN")
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

# Crea un objeto de la clase Shodan con la clave de API
api = shodan.Shodan(api_key)

# Pide al usuario qué quiere buscar en Shodan
query = input("Ingresa lo que quieres buscar en Shodan: ")

# Trata de convertir la cadena de entrada a una dirección IP
try:
    ip = ipaddress.ip_address(query)
    # Si la conversión es exitosa, significa que la cadena de entrada es una dirección IP
    # Por lo tanto, obtiene toda la información disponible sobre esa IP en Shodan
    try:
        host_info = api.host(query)
        # Declara una lista para almacenar las vulnerabilidades conocidas (CVE)
        cves_list = []
        if ip:
            f = open(query + ".txt", 'w', encoding="utf-8")
            # rest of the code
        else:
            print("Please enter a valid IP address")
        # Recorre cada resultado y muestra la información en pantalla y en el archivo
        for item in host_info['data']:
            print(colored("IP: ","yellow") + colored(item['ip_str'],"white") + colored(":","white") + str(colored(item['port'],"white")))
            print("IP: " + item['ip_str'] + ":" + str(item['port']) , file = f)
            if 'product' in item is not None:
                print(colored("Servicio:","yellow"), colored(item['product'],"green"))
                print("Servicio:", item['product'], file = f)
            else:
                print(colored("Servicio:","yellow") + colored("El Servicio No Esta Disponible","red"))
                print("Servicio: El Servicio No Esta Disponible" , file = f)
            if "http" in item is not None:
                print(((colored("Titulo Nombre Pagina: ","yellow")) + colored(item["http"]["title"],"cyan")))
                print(colored("Banner: Código de estado HTTP:","yellow"),colored(item["http"]["status"],"green"))
                print(f'Banner: Código de estado HTTP: {item["http"]["status"]}' , file = f)
            else:
                print(colored("Titulo: ","yellow") + colored("Nombre Pagina[No Encontrado]","red"))
                print("Titulo : Nombre Pagina[No Encontrado]" , file = f)
                print(colored("Codigo de estado HTTP: ","yellow") + colored("UNKOWN","red"))
                print("Codigo de estado HTTP: UNKOWN" , file = f)
            if "os" in item is not None:
                print(colored("Sistema Operativo:","yellow") , colored(item[("os")],"cyan"))
                print(f'Sistema Operativo: {item["os"]}' , file = f)
            else:
                print(colored("Sistema Operativo: No Es Una Computadora","blue"))
                print("Sistema Operativo: No Es Una Computadora" , file = f)
            print(colored("Organización:","yellow"), colored(item['org'],"cyan"))            
            print("Organización:", (item['org'],"cyan"), file = f)
            print(colored("Region:","yellow"), colored(item['location']['country_code'],"white")) 
            print(colored("Ciudad:","yellow"), colored(item['location']['city'],"white") + "\n")            
            print("Ciudad:", item['location']['city'] + "\n", file = f)
            # Intenta acceder a la lista de vulnerabilidades conocidas (CVE)
            try:
                cves = item['vulns']
                cves_list.extend(cves)  # Agrega las vulnerabilidades a la lista
            except KeyError:
                # Si no hay vulnerabilidades o la información no está disponible, no hace nada
                pass
        # Si se encontraron vulnerabilidades conocidas, las muestra en pantalla
        if cves_list:
            print(colored('CVE:',"red"))
            print('ES VULNERABLE CVE-XXXX', file = f)  # Muestra un título para la lista de CVE
            cves = ' - '.join([colored(cve, "red") for cve in cves_list])  # Une la lista de CVE en una sola cadena
            print(f'{cves}')
    except shodan.APIError as e:
        print("Error de la API:", e)
except ValueError:
    # Si no se puede convertir la cadena de entrada a una dirección IP, significa que se trata de una búsqueda normal en Shodan
    pass
finally:
    # Código que se ejecuta siempre al final de la operación
    # Realiza la búsqueda
    try:
        results = api.search(query)
        # Trata de abrir el archivo para escribir en él
        try:
            if query is not None:
               with open(query + ".txt", "w", encoding="utf-8") as f:
                # Recorre cada resultado y escribe la información en el archivo y en pantalla
                for result in results['matches']:
                    f.write("IP: " + result['ip_str'] + ":" + str(result['port']))
                    f.write("\n")
                    if 'product' in result is not None:
                        f.write("Servicio: " + result['product'] + "\n")
                    else:
                        f.write("Servicio: El Servicio No Esta Disponible\n")
                    if 'http' in result and result['http'] is not None and 'title' in result['http'] and result["http"]["title"] is not None:
                        f.write(f'Titulo: Nombre Pagina: {result["http"]["title"]}')
                        f.write("\n")
                        f.write(f'Banner: Código de estado HTTP: {result["http"]["status"]}')
                        f.write("\n")
                    else:
                        f.write("Titulo : Nombre Pagina: No Encontrado")
                        f.write("\n")
                        f.write("Codigo de estado HTTP: UNKOWN")
                        f.write("\n")
                    f.write("Organización: " + result['org'] + "\n")
                    if "os" in result is not None:
                        f.write(f'Sistema Operativo: {result["os"]}')
                    else:
                        f.write("Sistema Operativo: No Es Una Computadora")
                    f.write("\n")
                    f.write("Región: " + result['location']['region_code'] + "\n")
                    f.write("Ciudad: " + result['location']['city'] + "\n")
                    f.write("\n")
                    print(colored("IP: ","yellow") + colored(result['ip_str'],"white") + colored(":","white") + str(colored(result['port'],"white")))
                    if 'product' in result is not None:
                        print(colored("Servicio: ","yellow"), colored(result['product'],"cyan"))
                    else:
                        print(colored("Servicio:","yellow") + colored("El Servicio No Esta Disponible","red"))
                    if  'http' in result and result['http'] is not None and 'title' in result['http'] and result["http"]["title"] is not None:
                        print(colored("Titulo Nombre Pagina: ","yellow") + colored(result["http"]["title"],"cyan"))
                        print(colored("Banner: ","yellow") + colored("Código de estado HTTP:","yellow") + colored(result["http"]["status"],"green"))
                    else:
                        print(colored("Titulo ","yellow") + colored("Nombre Pagina[No Encontrado]","red"))
                        print(colored("Codigo de estado HTTP: ","yellow") + colored("UNKOWN","red"))
                    print(colored("Organización: ","yellow"), colored(result['org'],"cyan"))
                    if "os" in result is not None:
                        print(colored("Sistema Operativo: ","yellow") + colored(result["os"],"cyan"))
                    else:
                        print(colored("Sistema Operativo: ","yellow") + coloread("No Es Una Computadora","red"))
                    print(colored("Región:","yellow"), colored(result['location']['country_code'],"white"))
                    print(colored("Ciudad:","yellow"), colored(result['location']['city'],"white"))
                    print(colored("Timestamp:","yellow"), colored(result['timestamp'],"cyan"))
                    print()
        # Si hay un error al abrir el archivo, muestra un mensaje de error
        except Exception as e:
            print("Error al abrir el archivo:", e)
    # Muestra un mensaje de error si la API devuelve un error
    except shodan.APIError as e:
        print("Error de la API:", e)
