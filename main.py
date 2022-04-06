import urllib3
import builtwith
from bs4 import BeautifulSoup

def download_html(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")
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
    for link in links:
        sp = download_html(url + links)
        books_prices = sp.find_all("div", class_="col col-8")

url = "https://www.casadellibro.com/libro-y-pelicula"
data = []
dataset_file = "dataset.csv"

#print(builtwith.builtwith(url))

# Descargamos la página web

print("Iniciamos la descarga de la web")

#Realizamos la descarga incial de la web
soup = download_html(url)


items = soup.find_all("div", class_="d-flex flex-column align-center pa-2 item")

print("Items encontrados: " + str(len(items)))


    #print(sp)
    
links = get_links(items)


for l in links:
    sp = download_html(url + l)
    print(sp)




#file = open("libros.html", "w", encoding='utf-8')
#file.write(str(soup))