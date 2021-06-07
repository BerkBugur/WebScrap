import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.request
# Ürün resim indirme sıkıntlı

con = sqlite3.connect("kontakt-az.db")
cursor = con.cursor()

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satıcı TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

k = 0
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}
#range te bulunan sayı sayfa sayısıdır.

for x in range(8):
    URL ="https://kontakt.az/offers/page/"
    Page = x
    New_Url = URL + str(x)+"/"
    r = requests.get(New_Url)
    k += 1  # Sayfa sayısı
    print("Sayfa sayisi:", Page)

    soup = BeautifulSoup(r.content, "html5lib")
    ürünler = soup.find_all("section", {"id": "product-list"})

    for ürün in ürünler:
        ürün= soup.find_all("div",{"class":"cart-item-horizontal"})
        z = 0
        for i in ürün:
            z += 1  # Ürün Sayısı
            ürün_ismi = i.find("div",{"class":"item-about"})
            ürün_ismi_devam = ürün_ismi.find("h4").find("a").text
            ürün_link = ürün_ismi.find("h4").find("a").get("href")

            ürün_satici_var_yok = ürün_ismi.find("ul", {"class": "title"}).find_all("li")

            ürün_satici_var_yok = str(ürün_satici_var_yok)
            üretici = "İstehsalçı"

            if ürün_satici_var_yok.find(üretici) != -1:
                ürün_satici = ürün_ismi.find("ul", {"class": "content"})
                ürün_satici_devam = ürün_satici.find("li").text
                ürün_satici_devam = ürün_satici_devam.replace(" ","")
                ürün_satici_devam = ürün_satici_devam.replace("\n", "")
            else:
                ürün_satici_devam = "Ürünün Satıcısı bulunmamakta."

            urun_resim = i.find("div",{"class":"item-image"}).find("img").get("src")


            ürün_fiyat = i.find("div",{"class":"price-action"}).find("p").text
            ürün_fiyat = ürün_fiyat.replace("M", "")
            ürün_fiyat = ürün_fiyat + "AZN"


            print(ürün_ismi_devam) # Ürün ismi
            print(ürün_link) # Ürün link
            print(ürün_satici_devam) # Ürün Saticisi
            print(urun_resim) # Resim Url
            print(ürün_fiyat) # Ürün Fiyat

            print("===================")

            try:
                response = requests.get(urun_resim)

                file = open("upload/" + str(k)+"-"+str(z)+".png", "wb")
                file.write(response.content)
                file.close()

            except:
                print(str(x) + "numaralı ürün linki hatalıdır.")
                print(urun_resim)

            def degerEkle():
                cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)",
                               (ürün_ismi_devam, ürün_satici_devam, ürün_fiyat, urun_resim))
                con.commit()


            degerEkle()
con.close()



