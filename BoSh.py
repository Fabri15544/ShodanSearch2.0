import shodan
import ipaddress

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
        f = open(query + ".txt", 'w')
        # Recorre cada resultado y muestra la información en pantalla y en el archivo
        for item in host_info['data']:
            if 'product' in item:
                print("Servicio:", item['product'])
                print("Servicio:", item['product'], file = f)
            else:
                print("Servicio: El Servicio No Esta Disponible")
                print("Servicio: El Servicio No Esta Disponible" , file = f)
            print("Puerto:", item['port'])
            print("Puerto:", item['port'], file = f)
            print("Sistema operativo:", item['os'])
            print("Sistema operativo:", item['os'], file = f)
            print("Organización:", item['org'])            
            print("Organización:", item['org'], file = f)
            print("Ciudad:", item['location']['city'] + "\n")            
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
            print('CVE:')
            print('CVE:', file = f)  # Muestra un título para la lista de CVE
            cves = ' - '.join(cves_list)  # Une la lista de CVE en una sola cadena
            print(f'{cves}')  # Muestra la cadena con los nombres de las CVE
            print(f'{cves}', file = f)
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
            with open(query + ".txt", "w") as f:
                # Recorre cada resultado y escribe la información en el archivo y en pantalla
                for result in results['matches']:
                    f.write("IP: " + result['ip_str'] + "\n")
                    if 'product' in result:
                        f.write("Servicio: " + result['product'] + "\n")
                    else:
                        f.write("Servicio: El Servicio No Esta Disponible\n")
                    f.write("Organización: " + result['org'] + "\n")
                    f.write("Puertos: " + str(result['port']) + "\n")
                    f.write("Región: " + result['location']['region_code'] + "\n")
                    f.write("Ciudad: " + result['location']['city'] + "\n")
                    f.write("\n")
                    print("IP:", result['ip_str'])
                    if 'product' in result:
                        print("Servicio:", result['product'])
                    else:
                        print("Servicio: El Servicio No Esta Disponible")
                    print("Organización:", result['org'])
                    print("Puertos:", result['port'])
                    print("Región:", result['location']['region_code'])
                    print("Ciudad:", result['location']['city'])
                    print("Timestamp:", result['timestamp'])
                    print()
        # Si hay un error al abrir el archivo, muestra un mensaje de error
        except Exception as e:
            print("Error al abrir el archivo:", e)
    # Muestra un mensaje de error si la API devuelve un error
    except shodan.APIError as e:
        print("Error de la API:", e)
