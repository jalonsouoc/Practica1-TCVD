from Scraper import Scraper
 

url = "http://www.aemet.es/es/eltiempo/prediccion/municipios"
dataset_file = "dataset.csv"
data = []

scraper = Scraper(url)

print("Inicio del proceso")
print("Inicio del proceso de obtención de datos")

data = scraper.get_provincias(url)

print("Datos obtenidos")
print("Finalizado el proceso de obtención de datos")

print("Inicio de la escritura del fichero")

scraper.write_csv(dataset_file, data)

print("Finalizada la escritura del fichero")
print("Proceso terminado")
