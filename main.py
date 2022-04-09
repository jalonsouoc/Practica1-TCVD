from Scraper import Scraper
 

url = "http://www.aemet.es/es/eltiempo/prediccion/municipios"
dataset_file = "dataset.csv"
data = []

scraper = Scraper(url)

print("Inicio del proceso")
#Realizamos la descarga incial de la web
data = scraper.get_provincias(url)

print("Datos obtenidos")
print("Escribiendo los datos en el fichero")

scraper.write_csv(dataset_file, data)

print("Proceso terminado")
