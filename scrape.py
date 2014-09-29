# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

# Allow command line arguments through sys
import sys


# Post to Wordpress
def post_to_wp(post_content, cred):
	# Set up wordpress to accept posts from script
	wp = Client(cred[0], cred[1], cred[2])
	
	
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
	try:
		urlf = open(sys.argv[1], 'r')
		urls = [x for x in urlf.readline()]
		if len(urls) == 0:
			print "Nothing to scrape"
			return

		wp_info = open(sys.argv[2], 'r')
		wp_cred = [x for x in wp_info.readline()]
		if len(wp_cred) != 3:
			print "Malformed file"
			return
		
		# Close files
		urlf.close()
		wp_info.close()
		
	except IOError:
		print "Not a file"
		return
	
	# Get the actual content and dump it to Wordpress
	for url in urls:
		if 'ameblo.jp' in url:
			post_to_wp(get_post_list_ameblo(url), wp_cred)
		elif 'sonymusic.co.jp' in url:
			post_to_wp(get_post_list_sonymusic(url), wp_cred)
		else:
			print "Malformed file"
