# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts


# Post ameblo posts to Wordpress
def post_to_wp_ameblo(post_content, cred):
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


# Post sonymusic posts to Wordpress
def post_to_wp_sonymusic(post_content, cred):
	# Set up wordpress to accept posts from script
	wp = Client(cred[0], cred[1], cred[2])



if __name__ == "__main__":
	pass
