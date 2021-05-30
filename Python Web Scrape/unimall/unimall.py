import requests
from bs4 import BeautifulSoup

URL = "https://unimall.az/endirimler/"

r=requests.get(URL)

soup = BeautifulSoup(r.content,"html5lib")

ürünler = soup.find_all("div",{"class":"grid-list"})


for ürün in ürünler:
    ürün = soup.find_all("div",{"class":"ty-column4"})
    for i in ürün:
        ürün_ismi = i.find("div",{"class":"ty-grid-list__item-name"})
        ürün_ismi_devam = ürün_ismi.find("a",{"class":"product-title"}).text

        ürün_fiyat = i.find("span",{"class":"ty-price-num"}).text
        ürün_satici = i.find("span",{"class":"link"})
        ürün_satici_devam = ürün_satici.find("a").text




        print(ürün_fiyat)
        print(ürün_ismi_devam)
        print(ürün_satici_devam)


