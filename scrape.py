# Beautiful Soup
from bs4 import BeautifulSoup
import requests

# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts


def get_post_list_ameblo(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text) 
	
	# Get all relevant div elements
	div_list = soup.find_all("div", {"class": "entry"})
	
	return div_list


def get_post_list_sonymusic(url):
	r = requests.get(url)


def post_to_wp(post_content, target, user, pw):
	# Set up wordpress to accept posts from script
	wp = Client(target, user, pw)
	
	
	# Dump each thing into a wordpress post
	for entry in post_content:
		new_post = WordPressPost()
		new_post.title = unicode(entry.find("h3").find("a").contents[0])
		
		new_post.content = u"***Begin Original Content Here***\u000D"
		
		for p in entry.find("div", {"class": "contents"}).find("div", {"class": "subContents"}).find("div", {"class": "subContentsInner"}):
			temp = unicode(p)
			if temp != "entryBottom" and not "google_ad_section" in temp:
				new_post.content += unicode(p)
		
		new_post.id = wp.call(posts.NewPost(new_post))
		
		# Publish the post
		new_post.post_status = 'publish'
		wp.call(posts.EditPost(new_post.id, new_post))



if __name__ == "__main__":
	urls = open('url_list.txt', 'r')
	wp_info = open('wp_info.txt', 'r')
	
	wp_cred = [x for x in wp_info.readline()]
	
	for url in url.readline():
		if 'ameblo.jp' in url:
			post_to_wp(get_post_list_ameblo(url), wp_cred[0], wp_cred[1], wp_cred[2])
		elif 'sonymusic.co.jp' in url:
			post_to_wp(get_post_list_sonymusic(url), wp_cred[0], wp_cred[1], wp_cred[2])
