import urllib3
import builtwith
from bs4 import BeautifulSoup

def download_html(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    return soup

# Recorremos las provincias españolas
def get_provincias(url):
    municipiosProvincia = []
    for  i in range(1, 53):
        print(url + "?p=" + str(i) + "&w=t")
        municipiosProvincia = get_municipios(url + "?p=" + str(i) + "&w=t")
        get_datos_provincia(municipiosProvincia)


# Obtenemos los municipios de cada provincia
def get_municipios(url):
    soup = download_html(url)
    items = soup.find_all("td")
    print("Municipios encontrados: " + str(len(items)))
    dataMunicipios = []
    for item in items:
        municipio = item.find_all("a", href=True)
        urlMunicipio = municipio[0]['href'].split('/')
        dataMunicipios.append([municipio[0].text.strip(), urlMunicipio[len(urlMunicipio) - 1]])
        return dataMunicipios

#Obtenemos los datos de los municipios por provincia
def get_datos_provincia(dataMunicipios):
    for municipio in dataMunicipios:
        get_prediccion_municipio(url + "/" + municipio[1])
 


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

    #Obtenemos el viento y la dirección 
    direccion = bs_municipio.find_all("div", class_="texto_viento")[0].text.strip()
    velocidad = bs_municipio.find_all("div", class_="texto_km_viento")[0].text.strip()

    print("Dirección del viento:" + direccion)
    print("Velocidad del viento:" + velocidad)

    #Obtenemos la sensación térmica
    sensacion = bs_municipio.find_all("td", class_="no_wrap nocomunes")[0].text.strip()
    print("Sensación térmica:" + sensacion)

    #Precipitación y cota de nieve
    precipitacion = bs_municipio.find_all("td", class_="nocomunes")[0].text.strip()
    nieve = bs_municipio.find_all("td", class_="nocomunes")[13].text.strip()
    print("Porcentaje precipitación:" + precipitacion)
    print("Cota de nieve:" + nieve)

    #Obtenemos el indice iuv
    #iuv_td = bs_municipio.find_all("span", class_="raduv_pred_nivel3")
    #iuv = iuv_td.find_all("span", class_="raduv_pred_nivel3")[0].text.strip()
    #print(iuv_td)


url = "http://www.aemet.es/es/eltiempo/prediccion/municipios"
data = []
dataset_file = "dataset.csv"


#print(builtwith.builtwith(url))

# Descargamos la página web

print("Iniciamos la descarga de la web")

#Realizamos la descarga incial de la web
get_provincias(url)






    #print(sp)
    
#links = get_links(items)


#for l in links:
    #sp = download_html("https://www.casadellibro.com/" + l)
#get_book_information("https://www.casadellibro.com/", links)





#file = open("libros.html", "w", encoding='utf-8')
#file.write(str(soup))