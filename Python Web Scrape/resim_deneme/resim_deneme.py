import urllib.request

from bs4 import BeautifulSoup
import requests



x = "ber142k"

response = requests.get("https://kontakt.az/wp-content/uploads/gallery-tum/0072566_e835161ffba968add8bbc8a2f264bacd_w.jpg")

file = open("upload/"+"sample_image.png", "wb")
file.write(response.content)
file.close()