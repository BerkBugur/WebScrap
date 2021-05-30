import requests
from bs4 import BeautifulSoup

URL="https://www.trendyol.com/telefon-x-c104025"

r= requests.get(URL)

soup = BeautifulSoup(r.content,"html5lib")

ürünler = soup.find_all("div",{"class": "p-card-wrppr"})

for ürün in ürünler:
    ürün_ad = ürün.find("span",{"prdct-desc-cntnr-ttl"}).text
    ürün_detay = ürün.find("span",{"prdct-desc-cntnr-name hasRatings"}).text
    ürün_fiyat_indirimli = ürün.find("div", {"prc-box-dscntd"}).text
    ürün_fiyat_indirimsiz = ürün.find("div",{"prc-box-sllng prc-box-sllng-w-dscntd"}).text
    print(ürün_ad, ürün_detay, ürün_fiyat_indirimsiz, ürün_fiyat_indirimli)


