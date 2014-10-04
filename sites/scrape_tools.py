# Beautiful Soup
from bs4 import BeautifulSoup
import requests
from json_dump import json_dump


# Scraper for ameblo.jp
def get_post_list_ameblo(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text) 
	
	# Get all relevant div elements
	div_list = [ [d] for d in soup.find_all("div", {"class": "entry"}) ]
	for x in range(0, len(div_list)):
		div_list[x].append(div_list[x][0].find("h3").find("a")['href'])
	
	return div_list


# Scraper for sonymusic.co.jp
def get_post_list_sonymusic(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	
	# Get the urls for the actual posts
	articles = soup.find("ul", {"class": "utilList"}).find_all("p", {"class": "listSubject"})
	urls_list = [ "%s%s" % (url, a.find('a')['href'][19:]) for a in articles ]
	pages = [ BeautifulSoup(requests.get(u).text) for u in urls_list ] 
	
	# Get relevant div elements
	div_list = [ [p.find("div", {"id": "infoDetailArea"})] for p in pages ]
	for x in range(0, len(urls_list)):
		div_list[x].append(urls_list[x])
	
	return div_list



if __name__ == "__main__":
	pass
