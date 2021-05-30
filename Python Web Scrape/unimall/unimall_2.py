import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.request


con = sqlite3.connect("unimall.db")
cursor = con.cursor()

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satıcı TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

k = 0
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}
#range te bulunan sayı sayfa sayısıdır.
for x in range(15):
    URL = "https://unimall.az/endirimler/?page="
    Page =x
    New_Url= URL+str(x)
    r = requests.get(New_Url)
    k += 1 # Sayfa sayısı
    print("Sayfa sayisi:",Page)

    soup = BeautifulSoup(r.content, "html5lib")
    ürünler = soup.find_all("div", {"class": "grid-list"})

    for ürün in ürünler:
        ürün = soup.find_all("div", {"class": "ty-column4"})
        z = 0
        for i in ürün:
            z += 1 #Ürün Sayısı
            ürün_ismi = i.find("div", {"class": "ty-grid-list__item-name"})
            ürün_ismi_devam = ürün_ismi.find("a", {"class": "product-title"}).text

            ürün_fiyat = i.find("span", {"class": "ty-price-num"}).text
            ürün_satici = i.find("span", {"class": "link"})
            ürün_resmi = i.find("meta", {"itemprop":"image"})
            ürün_resmi_devam = ürün_resmi.get("content")
            ürün_satici_devam = ürün_satici.find("a").text

            print("Ürün Resmi Link->",ürün_resmi_devam)
            print("Ürün Fiyat->", ürün_fiyat)
            print("Ürün İsmi->", ürün_ismi_devam)
            print("Ürün Satıcısı->", ürün_satici_devam)
            print("--------")
            urllib.request.urlretrieve(ürün_resmi_devam,"upload/"+str(k)+"-"+str(z)+".jpg")

            def degerEkle():
                cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)",
                               (ürün_ismi_devam, ürün_satici_devam, ürün_fiyat, ürün_resmi_devam))
                con.commit()


            degerEkle()

con.close()
