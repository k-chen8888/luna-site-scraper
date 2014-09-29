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


if __name__ == "__main__":
	pass
