import requests
from bs4 import BeautifulSoup
import urllib.request
import sqlite3


con = sqlite3.connect("cinici-az.db")

Cinici_Url = "https://cinici.az"



cursor = con.cursor()
def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satici TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()



k=0
x = 1
#range te bulunan sayı sayfa sayısıdır.
for x in range(3):
    URL = "https://cinici.az/collection/?discount=true&page="
    Page = x
    New_Url = URL + str(x)
    r = requests.get(New_Url)
    k += 1  # Sayfa sayısı
    print("Sayfa sayisi:", Page)
    print("Sayfa Url:", New_Url)

    r = requests.get(New_Url)
    soup = BeautifulSoup(r.content, "html5lib")
    ürünler = soup.find_all("div", {"class": "woman-collection-right-bottom"})

    for ürün in ürünler:
        ürün_link = ürün.find_all("a",{"class":"product-item"})
        for i in ürün_link:
            x += 1
            ürün_link_devam = Cinici_Url+i.get("href")

            ürün_resim = i.find("div",{"class":"product-image-container"})
            ürün_resim_devam = Cinici_Url+ürün_resim.find("img").get("src")
            ürün_resim_asil = ürün_resim_devam

            ürün_isim = i.find("h5",{"class":"name"}).text

            ürün_satici = "Cinici" # Ürün satıcısı yazmıyor.
            ürün_fiyat = i.find("span",{"class":"pink"}).text
            ürün_fiyat = ürün_fiyat.replace("₼", "")
            ürün_fiyat = ürün_fiyat.replace(" ", "")+ " AZN"


            try:
                response = requests.get(ürün_resim_asil)

                file = open("upload/" + str(k)+"-"+str(x)+".png", "wb")
                file.write(response.content)
                file.close()
            except:
                print(str(x)+"numaralı ürün linki hatalıdır.")


            def degerEkle():
                cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)", (ürün_isim,ürün_satici,ürün_fiyat,ürün_resim_asil))
                con.commit()

            degerEkle()


            print(ürün_fiyat)
            print(ürün_isim)
            print(ürün_resim_asil)
            print(ürün_link_devam)
            print("=============")

con.close()