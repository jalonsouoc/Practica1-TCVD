import urllib3
import builtwith
from bs4 import BeautifulSoup

def download_html(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    return soup

def get_links(items):
    links = []
    # Obtenemos las tarjetas de cada libro
    for item in items:
        itemLink = item.find_all("a", href=True, class_="d-flex v-card v-card--flat v-card--link v-sheet theme--light rounded-0")
        #Obtenemos los enlaces de cada tarjeta
        links.append(itemLink[0]['href'])
        
    return links

def get_book_information(url, links):
    books = []
    for link in links:
        print(url + link)
        sp = download_html(url + link)
       
        books_info = sp.find_all("div", class_="product-info")
        for book in books_info:
            name = book.find_all("h1", class_="text-h4 mb-2")
            print(name[0].text.strip())
            books.append({name})




url = "http://www.aemet.es/es/eltiempo/prediccion/municipios?p=38&w=t"
data = []
dataset_file = "dataset.csv"

#print(builtwith.builtwith(url))

# Descargamos la página web

print("Iniciamos la descarga de la web")

#Realizamos la descarga incial de la web
soup = download_html(url)


items = soup.find_all("td")


print("Items encontrados: " + str(len(items)))
dataMunicipios = []
for item in items:
    municipio = item.find_all("a", href=True)
    urlMunicipio = municipio[0]['href'].split('/')
    dataMunicipios.append([municipio[0].text.strip(), urlMunicipio[len(urlMunicipio) - 1]])
 

def get_prediccion_municipio(url):
    bs_municipio = download_html(url)
    #Obtenemos la fecha
    fecha = bs_municipio.find_all("th", class_="borde_izq_dcha_fecha")[0].text.strip()
    print(fecha)

    #Obtenemos las horas
    hora = bs_municipio.find_all("div", class_="fuente09em")[0].text.strip()
    print(hora)

    #Obtenemos el tiempo
    tiempo_div = bs_municipio.find_all("div", class_="width47px margen_auto_horizontal")
    tiempo = tiempo_div[0].find("img").get('title')
    print(tiempo)

    #Obtenemos los grados
    temperatura = bs_municipio.find_all("div", class_="no_wrap")[0].text.strip()
    print(temperatura)

    # Obtenemos la temperatura mínima y máxima y la sensación térmica
    
    comunes = bs_municipio.find_all("td", class_="alinear_texto_centro no_wrap comunes")
    min_max = comunes[0]
    sensacion_min_max = comunes[7]
    print(min_max)
    minimo = min_max.find_all("span", class_="texto_azul")[0].text.strip()
    maximo  = min_max.find_all("span", class_="texto_rojo")[0].text.strip()
    print("Temperatura mínima:" + minimo)
    print("Temperatura máxima:" + maximo)
    sensacion_minima = sensacion_min_max.find_all("span", class_="texto_azul")[0].text.strip()
    sensacion_maxima  = sensacion_min_max.find_all("span", class_="texto_rojo")[0].text.strip()
    print("Sensación mínima:" + sensacion_minima)
    print("Sensación máxima:" + sensacion_maxima)


    #Obtenemos la humedad
    humedad_min_max = bs_municipio.find_all("td", class_="alinear_texto_centro comunes")[0]
    humedad_min = humedad_min_max.find_all("span", class_="texto_marron")[0].text.strip()
    humedad_max = humedad_min_max.find_all("span", class_="texto_verde")[0].text.strip()

    print("Humedad mínima:" + humedad_min)
    print("Humedad máxima:" + humedad_max)


for municipio in dataMunicipios:
    print(municipio[0])
    url_municipio = "http://www.aemet.es/es/eltiempo/prediccion/municipios/" + municipio[1]
    get_prediccion_municipio(url_municipio)






    #print(sp)
    
#links = get_links(items)


#for l in links:
    #sp = download_html("https://www.casadellibro.com/" + l)
#get_book_information("https://www.casadellibro.com/", links)





#file = open("libros.html", "w", encoding='utf-8')
#file.write(str(soup))