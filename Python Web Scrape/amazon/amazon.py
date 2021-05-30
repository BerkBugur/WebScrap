import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com.tr/gp/bestsellers/electronics/13709880031/ref=zg_bs_nav_1_electronics"

r = requests.get(URL)

soup = BeautifulSoup(r.content, "html5lib")

ürünler = soup.find_all("li", {"class": "zg-item-immersion"})
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

for ürün in ürünler:
    ürün_link = ürün.find_all("div", {"class": "a-section a-spacing-none aok-relative"})
    for i in ürün_link:
        link = i.find("span", {"class": "zg-item"})
        link_devam = link.a.get("href")
        link_domain = "http://amazon.com.tr"
        link_tamami = link_domain + link_devam

        detay = requests.get(link_tamami, headers=headers)
        detay_soup = BeautifulSoup(detay.text, "html5lib")
        teknik_ayrintilar = detay_soup.find_all("table",{"class" : "a-keyvalue prodDetTable"})

        for teknik in teknik_ayrintilar:
            detaylar =teknik.find_all("tr")
            for i in detaylar:
                try:
                    etiket = i.find("th",{"class":"a-color-secondary a-size-base prodDetSectionEntry"}).text
                    deger = i.find("td",{"class":"a-size-base prodDetAttrValue"}).text
                    deger = deger.replace("\n", "")
                    deger = deger.replace("  ", "")
                    etiket = etiket.replace("\n", "")
                    etiket = etiket.replace("  ","")
                    print(etiket,": " ,deger)
                except:
                    print("")