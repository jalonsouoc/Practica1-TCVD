import urllib3
from bs4 import BeautifulSoup

url = "https://www.youtube.com/"
data = []
dataset_file = "dataset.csv"

# Descargamos la página web
http = urllib3.PoolManager()
response = http.request('GET', url)
soup = BeautifulSoup(response.data.decode('utf-8'), "lxml")

a = soup.find_all('div')

#file = open("youtube.html", "w", encoding='utf-8')
#file.write(str(soup))