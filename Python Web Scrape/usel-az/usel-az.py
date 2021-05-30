import requests
from bs4 import BeautifulSoup
import urllib.request
import sqlite3

con = sqlite3.connect("usel-az.db")
URL = "https://usel.az/az/specials/?limit=100"

r = requests.get(URL)
soup = BeautifulSoup(r.content, "html5lib")

ürünler = soup.find_all("div", {"class": "row"})

cursor = con.cursor()
def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satici TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}
x = 0
for ürün in ürünler:
    ürün_link = ürün.find_all("div", {"class": "product-layout product-grid col-lg-3 col-sm-4 col-xs-6"})
    for i in ürün_link:

        x += 1
        link = i.find("div", {"class": "image"})
        link_devam = link.a.get("href")

        detay = requests.get(link_devam)
        detay_soup = BeautifulSoup(detay.text, "html5lib")
        teknik_ayrintilar = detay_soup.find("div", {"class": "col-sm-8 prod_right"})
        resim_bilgisi = detay_soup.find("div", {"class": "col-sm-4 prod_left"})

        resim = resim_bilgisi.find("img", {"class": "main_image"})
        resim_devam = resim.get("src")

        ürün_fiyati = detay_soup.find("h2", {"class": "price_spec"})
        ürün_fiyat = ürün_fiyati.find("span", {"class": "new-prices"}).text

        ürün_isim = teknik_ayrintilar.find("h2", {"class": "hidden-xs"}).text
        ürün_sahibi = teknik_ayrintilar.find("ul", {"col-sm-6"})
        try:
            ürün_sahibi_isim = ürün_sahibi.find("li").a.text
        except:
            ürün_sahibi_isim = ("Üretici belli değil.")

        try:
            urllib.request.urlretrieve(resim_devam,"upload/"+str(x)+".jpg")
        except:
            print(str(x)+"numaralı ürün linki hatalıdır.")

        resim_devam = resim_devam.replace(" ", "")
        print(resim_devam)
        print(ürün_isim)
        print(ürün_sahibi_isim)
        print(ürün_fiyat)
        print("-------------")

        def degerEkle():
            cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)", (ürün_isim,ürün_sahibi_isim,ürün_fiyat,resim_devam))
            con.commit()

        degerEkle()

con.close()

