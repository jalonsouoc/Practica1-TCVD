from asyncore import write
import urllib3
import builtwith
from bs4 import BeautifulSoup
import bs4
import csv
from DiaHoraMunicipio import DiaHoraMunicipio

def download_html(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    return soup

# Recorremos las provincias españolas
def get_provincias(url):
    municipiosProvincia = []
    datosProvincia = []
    for  i in range(1,2): # for  i in range(1, 51):
        print(url + "?p=" + str(i) + "&w=t")
        municipiosProvincia = get_municipios(url + "?p=" + str(i) + "&w=t", "Nombre provincia")
        prov = get_datos_provincia(municipiosProvincia) # Obtener la provincia y pasarla
        for dato in prov:
            datosProvincia.append(dato)
        
        
    return datosProvincia
    #Añadir a ceuta y melilla


# Obtenemos el nombre y la url de cada provincia
def get_municipios(url, provincia):
    soup = download_html(url)
    items = soup.find_all("td")
    print("Municipios encontrados: " + str(len(items)))
    dataMunicipios = []
    for item in items:
        municipio = item.find_all("a", href=True)
        urlMunicipio = municipio[0]['href'].split('/')
        dataMunicipios.append([municipio[0].text.strip(), provincia ,urlMunicipio[len(urlMunicipio) - 1]])
        
    return dataMunicipios

#Obtenemos los datos de los municipios por provincia
def get_datos_provincia(dataMunicipios):
    data = []
    for municipio in dataMunicipios:
        urlMunicipio = url + "/" + municipio[2] + "#detallada"
        predicciones = get_prediccion_municipio(urlMunicipio, municipio[0], municipio[1])
        for pred in predicciones:
            data.append(pred)
        
    return data
 


def get_prediccion_municipio(url, municipio, provincia):

    datosMunicipio = []
    bs_municipio = download_html(url)

    fechas = bs_municipio.find_all("th", class_="borde_izq_dcha_fecha")
    nFechas = len(fechas)
    indiceFechaActual = 0

    horas = bs_municipio.find_all("div", class_="fuente09em")
    # Cantidad de horas de la ventana
    nHoras = len(bs_municipio.find_all("th", class_="borde_izq_dcha_estado_cielo no_wrap"))

    #Obtenemos todos los tiempos de los días
    tiempo_div = bs_municipio.find_all("div", class_="width47px margen_auto_horizontal")

    #Obtenemos todas las temperaturas 
    temperatura_div = bs_municipio.find_all("div", class_="no_wrap")

    for i in range(nHoras):
        fecha = fechas[indiceFechaActual].text.strip()

        # Cómo hay horas que no vienen cumplimentadas, añadimos horas vacías al final del vector
        if len(horas) > i:
            hora = horas[i].text.strip()
        else:
            hora = " "

        if "24" in hora or " " in hora:
            indiceFechaActual = indiceFechaActual+1

        #Obtenemos el tiempo del día y la fecha
        if i <  len(tiempo_div):
            tiempo = tiempo_div[i].find("img").get('title')
        else:
            tiempo = " "
        

        #Obtenemos la temperatura
        if i < len(temperatura_div):
            temperatura = bs_municipio.find_all("div", class_="no_wrap")[i].text.strip()
        else:
            temperatura = " "

       

        diaHora = DiaHoraMunicipio(municipio, provincia, fecha, hora, tiempo, temperatura)
        
        datosMunicipio.append(diaHora)

    return datosMunicipio


def write_csv(filename, data):
    file = open(filename, "w+")
    for i in range(len(data)):
        for item in data[i]:
            file.write(item + ";")
        file.write("\n")
    
 

url = "http://www.aemet.es/es/eltiempo/prediccion/municipios"
dataset_file = "dataset.csv"


#print(builtwith.builtwith(url))

# Descargamos la página web

print("Iniciamos la descarga de la web")

#Realizamos la descarga incial de la web
data = get_provincias(url)

write_csv(dataset_file, data)






    #print(sp)
    
#links = get_links(items)


#for l in links:
    #sp = download_html("https://www.casadellibro.com/" + l)
#get_book_information("https://www.casadellibro.com/", links)





#file = open("libros.html", "w", encoding='utf-8')
#file.write(str(soup))


"""      # Obtenemos la temperatura mínima y máxima y la sensación térmica
        
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
"""