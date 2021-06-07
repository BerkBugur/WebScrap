import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.request
import urllib

URL = "https://shop.az/discounts"

r = requests.get(URL)
soup = BeautifulSoup(r.content, "html5lib")
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

con = sqlite3.connect("shop-az.db")
cursor = con.cursor()
def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satıcı TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

ürünler = soup.find_all("div", {"class": "col-md-48"})

x = 0
for ürün in ürünler:
    ürün_link = ürün.find_all("div", {"class": "col-md-20 col-lg-15 col-xl-12 hasDiscount-1 _products"})
    for i in ürün_link:
        x += 1
        link = i.find("a",{"class":"thumbnail-link"}).get("href")
        #print(link)
        detay = requests.get(link, headers=headers)
        detay_soup = BeautifulSoup(detay.text, "html5lib")
        teknik_ayrintilar = detay_soup.find("div", {"id": "product_Maininfo"})
        ürün_resim = teknik_ayrintilar.find("div",{"class":"productMainImage"}).find("img",{"itemprop":"image"}).get("src")
        ürün_resim = str(ürün_resim)
        ürün_detay = teknik_ayrintilar.find("div",{"class":"centerly"})
        ürün_isim = ürün_detay.find("span",{"class":"product_Name work-break-w"}).text
        ürün_satici = ürün_detay.find("span",{"class":"product_shop_Name"}).find("a").text
        ürün_fiyat = ürün_detay.find("p",{"class":"product_Price"}).text
        print(ürün_isim)
        print(ürün_resim)
        print(ürün_satici)
        print(ürün_fiyat)
        print("=================")

        def degerEkle():
            cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)", (ürün_isim,ürün_satici,ürün_fiyat,ürün_resim))
            con.commit()

        degerEkle()

        try:
            response = requests.get(ürün_resim)

            file = open("upload/" + str(x) + ".png", "wb")
            file.write(response.content)
            file.close()



        except:
            print(str(x)+"numaralı ürün linki hatalıdır.")


con.close()