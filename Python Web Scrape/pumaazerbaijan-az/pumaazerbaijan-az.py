from bs4 import BeautifulSoup
import requests
import urllib.request
import sqlite3

con = sqlite3.connect("pumaazerbaijan-az.db")
URL = "https://pumaazerbaijan.az/az/shop/all?gen=all&search=puma&attr=new&discount=25&limit=1000"
Puma_Url="https://pumaazerbaijan.az"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

cursor = con.cursor()
def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (isim TEXT, satici TEXT, fiyat TEXT, resim TEXT)")

tabloolustur()

x=0
r=requests.get(URL)
soup = BeautifulSoup(r.content,"html5lib")

ürünler = soup.find_all("div",{"id":"product-grid__container"})


for ürün in ürünler:
    ürün_block = soup.find_all("div",{"class":"col-6 col-lg-3"})
    for i in ürün_block:
        x += 1
        link = i.find("a",{"class":"quickview hidden-xs-down product-view"})
        link_devam = link.get("href")
        link_asil = Puma_Url+link_devam
        satici = i.find("meta",{"itemprop":"brand"})
        satici_devam= satici.get("content")

        ürün_fiyat = i.find("div",{"class":"prices__base"})
        ürün_fiyat_devam = ürün_fiyat.find("span",{"class":"prices__base-value"}).text
        ürün_fiyat_asil = ürün_fiyat_devam+" AZN"

        ürün_resim = i.find("a",{"class":"grid__product-thumbnail"})
        ürün_resim_devam = ürün_resim.find("source")
        ürün_resim_asil = Puma_Url + ürün_resim_devam.get("srcset")

        ürün_ismi = i.find("span",{"itemprop":"name"}).text

        try:
            urllib.request.urlretrieve(ürün_resim_asil,"upload/"+str(x)+".jpg")
        except:
            print(str(x)+"numaralı ürün linki hatalıdır.")

        def degerEkle():
            cursor.execute("INSERT INTO urunler VALUES(?,?,?,?)", (ürün_ismi,satici_devam,ürün_fiyat_asil,ürün_resim_asil))
            con.commit()

        degerEkle()
        print(satici_devam) # Satıcı
        print(link_asil)    # Ürün Link
        print(ürün_fiyat_asil) #Ürün Fiyat
        print(ürün_resim_asil) # Ürün Resim Link
        print(ürün_ismi)       # Ürün İsmi
        print("==================")

con.close()

