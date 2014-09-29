# Beautiful Soup
from bs4 import BeautifulSoup
import requests


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
	pages = []
	for a in articles:
		new_url = "%s%s" % (url, a.find('a')['href'][19:])
		pages.append(BeautifulSoup(requests.get(new_url).text))
	
	# Get relevant div elements
	div_list = [ p.find("div", {"id": "infoDetailArea"}) for p in pages ]
	
	return div_list


if __name__ == "__main__":
	get_post_list_sonymusic("http://www.sonymusic.co.jp/artist/Lunaharuna/")
