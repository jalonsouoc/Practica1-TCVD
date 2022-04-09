import urllib3
from bs4 import BeautifulSoup
import time
from DiaHoraMunicipio import DiaHoraMunicipio

class Scraper():

    def __init__(self, url):
            self.url = url



    #Método encargado de descargarse las webs
    def download_html(self,url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "lxml")
        return soup

    # Método que recorre las provincias españolas obteniendo los datos de cada provincia
    def get_provincias(self,url):
        municipiosProvincia = []
        datosProvincia = []
        for  i in range(1, 51):
            urlProvincia = url + "?p=" + str(i) + "&w=t"
            municipiosProvincia = self.get_municipios(urlProvincia)
            prov = self.get_datos_provincia(municipiosProvincia)
            for dato in prov:
                datosProvincia.append(dato)
            
        # Para las ciudades autónomas al no tener provincias se recorren como un municipio más
        for j in range(51, 53):
            urlProvincia = url + "?p=" + str(j) + "&w=t"
            start_time = time.time()
            ciudad = self.get_ciudad_autonoma(urlProvincia)
            datosPredic = self.get_prediccion_municipio(ciudad[2], ciudad[0], ciudad[1])
            for dato in datosPredic:
                datosProvincia.append(dato)
            time.sleep(2)
            end_time = time.time()
            print("Tiempo transcurrido para la ciudad autónoma: " + str(round(((end_time - start_time) / 60), 2)) + "minutos" )
            
        return datosProvincia


    # Método que obtiene los municipios de cada provincia y su url
    def get_municipios(self,url):
        soup = self.download_html(url)
        prvoincia_h2 = soup.find_all("h2", class_="titulo")[0].text.strip()
        provincia = prvoincia_h2.split(".", 2)[1].strip()
        items = soup.find_all("td")
        print(provincia)
        print("Municipios: " + str(len(items)))
        print("URL: " + url)
        
        dataMunicipios = []
        for item in items:
            municipio = item.find_all("a", href=True)
            urlMunicipio = municipio[0]['href'].split('/')
            dataMunicipios.append([municipio[0].text.strip(), provincia ,urlMunicipio[len(urlMunicipio) - 1]])
            
        return dataMunicipios

    # Método que obtiene los datos de la ciudades autónomas
    def get_ciudad_autonoma(self,url):
        soup = self.download_html(url)
        prvoincia_h2 = soup.find_all("h2", class_="titulo")[0].text.strip()
        provincia = prvoincia_h2.split(".", 2)[1].strip()
        print(provincia)
        print("Ciudad Autónoma")
        print("URL: " + url)
        datosCiudad = [provincia, provincia, url]

        return datosCiudad
        

    #Método que obtiene las predicciones de todos los municipios de una provincia
    def get_datos_provincia(self, dataMunicipios):
        data = []
        start_time = time.time()
        for municipio in dataMunicipios:
            urlMunicipio = self.url + "/" + municipio[2] + "#detallada"
            predicciones = self.get_prediccion_municipio(urlMunicipio, municipio[0], municipio[1])
            for pred in predicciones:
                data.append(pred)
            time.sleep(2)
        
        end_time = time.time()

        print("Tiempo transcurrido para la provincia: " + str(round(((end_time - start_time) / 60), 2)) + "minutos" )
        return data
    

    # Método que obtiene los datos de cada municipio que se le pasa como parámetro
    def get_prediccion_municipio(self, url, municipio, provincia):

        datosMunicipio = []
        bs_municipio = self.download_html(url)

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

        #Obtenenmos la probabilidad de precipitación y cota de nieve
        div_nocomunes = bs_municipio.find_all("td", class_="nocomunes")

        precipitacion_div = div_nocomunes[0:nHoras]
        nieve_div = div_nocomunes[nHoras:nHoras*2]
        racha_max_div = div_nocomunes[nHoras*3:nHoras*4]

        #Obtenemos la temperatura  y la sensación térmica mínima y máxima
        min_max_div = bs_municipio.find_all("td", class_="alinear_texto_centro no_wrap comunes")

        #Obtenemos la humedad máxima y mínima
        humedad_min_max_div = bs_municipio.find_all("td", class_="alinear_texto_centro comunes")

        #Obtenemos el viento y la dirección 
        dir_viento_div = bs_municipio.find_all("div", class_="texto_viento")
        vel_viento_div = bs_municipio.find_all("div", class_="texto_km_viento")


        for i in range(nHoras):
            fecha = fechas[indiceFechaActual].text.strip()

            # Cómo hay horas que no vienen cumplimentadas, añadimos horas vacías al final del vector
            if len(horas) > i:
                hora = horas[i].text.strip()
            else:
                hora = " "


            #Obtenemos el tiempo del día y la fecha
            if i <  len(tiempo_div):
                tiempo = tiempo_div[i].find("img").get('title')
            else:
                tiempo = " "
            

            #Obtenemos la temperatura
            if i < len(temperatura_div):
                temperatura = temperatura_div[i].text.strip()
            else:
                temperatura = " "

            #Obtenemos la probabilidad de precipitación
            precipitacion = precipitacion_div[i].text.strip()

            #Obtenenmos  la cota de nieve
            nieve = nieve_div[i].text.strip()

            #Obtenemos la racha máxima de viento
            racha_max = racha_max_div[i].text.strip()

            #Obtenemos la temperatura mínima y máxima
            temp_min = min_max_div[indiceFechaActual].find_all("span", class_="texto_azul")[0].text.strip()
            temp_max = min_max_div[indiceFechaActual].find_all("span", class_="texto_rojo")[0].text.strip()

            #Obtenemos la sensación térmica mínima y máxima
            sens_min = min_max_div[indiceFechaActual + nFechas].find_all("span", class_="texto_azul")[0].text.strip()
            sens_max  = min_max_div[indiceFechaActual + nFechas].find_all("span", class_="texto_rojo")[0].text.strip()

            #Obtenemos la humedad mínima y máxima
            humedad_min = humedad_min_max_div[indiceFechaActual].find_all("span", class_="texto_marron")[0].text.strip()
            humedad_max = humedad_min_max_div[indiceFechaActual].find_all("span", class_="texto_verde")[0].text.strip()

            #Obtenemos el viento y la dirección 
            dir_viento = dir_viento_div[i].text.strip()
            vel_viento = vel_viento_div[i].text.strip()

            diaHora = DiaHoraMunicipio(municipio, provincia, fecha, hora, tiempo, temperatura, precipitacion, nieve, temp_min, temp_max, sens_min, sens_max, humedad_min, humedad_max, dir_viento, vel_viento, racha_max)
            
            datosMunicipio.append(diaHora)

            # LLeva el control del día en el que estamos, si la últim ahora contiene 24 h ó está vacío significa que el día ha terminado
            if "24" in hora or " " in hora:
                indiceFechaActual = indiceFechaActual+1

        return datosMunicipio


    #Método que realiza la escritura en el fichero
    def write_csv(filename, data):
        file = open(filename, "w+")
        file.write("Municipio;Provincia;Día;Horario;Tiempo;Temperatura;Probabilidad precipitación; Cota de nieve; Temperatura mínima; Temperatura máxima; Sensación térmica mínima; Sensación térmica máxima; Humedad mínima; Humedad máxima; Dirección del viento; Velocidad del viento; Racha máxima de viento;")
        for i in range(len(data)):
            for item in data[i]:
                file.write(item + ";")
            file.write("\n")
