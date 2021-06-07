import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.request

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}
Maxi_Url="https://maxi.az"
con = sqlite3.connect("maxi-az.db")
cursor = con.cursor()

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satıcı TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

k = 0
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

#range te bulunan sayı sayfa sayısıdır.
for x in range(15):
    URL= "https://maxi.az/actions/discount/?PAGEN_100="
    Page = x
    New_Url = URL + str(x)
    r = requests.get(New_Url)
    k += 1  # Sayfa sayısı
    print("Sayfa sayisi:", Page)

    soup = BeautifulSoup(r.content, "html5lib")
    ürünler = soup.find_all("div", {"class": "cont-cat-in"})

    for ürün in ürünler:
        ürün = soup.find_all("div", {"class": "one-cat-item"})
        z = 0
        for i in ürün:
            z += 1  # Ürün Sayısı
            ürün_link = i.find("div",{"class":"one-cat-item-tit"}).find("a")
            ürün_link_devam = ürün_link.get("href")
            ürün_link_devam = Maxi_Url + str(ürün_link_devam)
            #print(ürün_link_devam)
            ürün_isim = ürün_link.text
            #print(ürün_isim)
            detay = requests.get(ürün_link_devam, headers=headers)
            detay_soup = BeautifulSoup(detay.text, "html5lib")
            teknik_ayrintilar = detay_soup.find("div", {"class": "char-atr"})
            ürün_satici = teknik_ayrintilar.find("span",{"itemprop":"brand"}).text
            #print(ürün_satici)
            ürün_resim = detay_soup.find("div",{"class":"product-info"})
            ürün_resim_devam = ürün_resim.find("div",{"class":"one-prod-slid-in"}).find("img").get("src")
            ürün_resim_devam = Maxi_Url+ürün_resim_devam
            print(ürün_resim_devam)
            ürün_fiyat = detay_soup.find("div",{"class":"price-prod-now"}).find("span").text + " AZN"
            print(ürün_fiyat)

            #urllib.request.urlretrieve(ürün_resim_devam, "upload/" + str(k) + "-" + str(z) + ".jpg")

            def degerEkle():
                cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)",
                               (ürün_isim, ürün_satici, ürün_fiyat, ürün_resim_devam))
                con.commit()


            degerEkle()
con.close()