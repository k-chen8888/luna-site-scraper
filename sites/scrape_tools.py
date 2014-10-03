# Beautiful Soup
from bs4 import BeautifulSoup
import requests
import json_dump


# Scraper for ameblo.jp
def get_post_list_ameblo(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text) 
	
	# Get all relevant div elements
	div_list = soup.find_all("div", {"class": "entry"})
	
	return div_list


# Scraper for sonymusic.co.jp
def get_post_list_sonymusic(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	
	# Get the urls for the actual posts
	articles = soup.find("ul", {"class": "utilList"}).find_all("p", {"class": "listSubject"})
	pages = [ BeautifulSoup(requests.get("%s%s" % (url, a.find('a')['href'][19:])).text) for a in articles ] 
	
	# Get relevant div elements
	div_list = [ p.find("div", {"id": "infoDetailArea"}) for p in pages ]	
	
	return div_list



if __name__ == "__main__":
	l = get_post_list_sonymusic("http://www.sonymusic.co.jp/artist/Lunaharuna/")
	json_dump(l, "sonymusic", "/json")
