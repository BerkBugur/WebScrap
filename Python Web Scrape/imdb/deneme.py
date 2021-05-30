import requests
from bs4 import BeautifulSoup

Url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
R = requests.get(Url)  # Post olursa veri aratma gibi yapabiliriz
BSoup = BeautifulSoup(R.text, "html5lib")
# print(BSoup)
# print(R.text)
List = BSoup.find("tbody", {"class": "lister-list"}).find_all("tr") #find_all !!

for film in List:
    name = film.find("td", {"class": 'titleColumn'}).a.text
    date = film.find("td",{"class": 'titleColumn'}).span.text
    rating = film.find("td",{"class": 'ratingColumn imdbRating'}).strong.text
    people = film.find("td", {"class": 'ratingColumn imdbRating'}).strong
    print("Film Adı:"+name+" Tarih-"+date+" Puan:"+rating)
