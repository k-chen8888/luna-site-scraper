# Beautiful Soup
from bs4 import BeautifulSoup
import requests

# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


r = requests.get("http://ameblo.jp/luna-luna-moonrise/")

soup = BeautifulSoup(r.text) 


# Get all relevant div elements
div_list = soup.find_all("div", {"class": "entry"})


# Dump each thing into a wordpress post
new_posts = []
i = 0
for entry in div_list:
	new_posts.append(WordPressPost())
	new_posts[i].title = entry.find("h3").find("a").contents[0]
	
	new_posts[i].content = "***Begin Original Content Here***\n"
	
	for p in entry.find("div", {"class": "contents"}).find("div", {"class": "subContents"}).find("div", {"class": "subContentsInner"}).find_all("p", {"class": "MsoNormal"}):
		new_posts[i].content += str(p)
	

	i += 1

print new_posts
