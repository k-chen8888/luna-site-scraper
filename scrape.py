from bs4 import BeautifulSoup
import requests

r = requests.get("http://ameblo.jp/luna-luna-moonrise/")

soup = BeautifulSoup(r.text)

print soup.prettify()
