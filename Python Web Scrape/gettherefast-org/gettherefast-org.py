import requests
from bs4 import BeautifulSoup
import urllib.request
import sqlite3

con = sqlite3.connect("gettherefast-org.db")




cursor = con.cursor()
def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satici TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177'}
x = 0
k = 0
#range te bulunan sayı sayfa sayısıdır.
for x in range(15):
    URL = "http://www.gettherefast.org/usaqlarin-fealiyyeti-ve-avadanliqlari/"
    Page = x
    New_Url= URL+str(x)+"/"
    r = requests.get(New_Url)
    k += 1 # Sayfa sayısı
    print("Sayfa sayisi:",Page)

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html5lib")

    ürünler = soup.find_all("div", {"class": "row"})
    for ürün in ürünler:
        ürün_link = ürün.find_all("div", {"class": "col-md-3"})
        for i in ürün_link:
            x += 1
            referans_link = i.find("a").get("href")
            #print(referans_link)
            ürün_isim = i.find("p",{"class":"title text-truncate"}).text
            #print(ürün_isim)

            detay = requests.get(referans_link)
            detay_soup = BeautifulSoup(detay.text, "html5lib")
            teknik_ayrintilar = detay_soup.find("article", {"class": "content-body"}).find("a").get("href")
            print(teknik_ayrintilar)
            alibaba = requests.get(teknik_ayrintilar,headers=headers)
            alibaba_soup = BeautifulSoup(alibaba.content,"html5lib")

            ürün_yeni_link = alibaba_soup.find_all("link", {"rel": "alternate"}).get("href")
            print(ürün_yeni_link)



