from bs4 import BeautifulSoup
import requests
import urllib.request

URL="https://usel.az/image/cache/catalog/00-00007242/addaadda-400x400-product_thumb.jpg"

x = "berk"

urllib.request.urlretrieve(URL,"upload/"+x+".jpg")