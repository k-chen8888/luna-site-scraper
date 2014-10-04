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
		new_post.title = unicode(entry[0].find("h3").find("a").contents[0])
		
		new_post.content = u"***Begin Original Content Here***\u000D"
		new_post.content += u"Posted on: " + unicode(entry[0].find("span", {"class": "date"}).contents[0]) + u"\u000D"
		new_post.content += u"<a href=\u0022" + entry[1] + u"\u0022>See original post</a>\u000D"

		for p in entry[0].find("div", {"class": "contents"}).find("div", {"class": "subContents"}).find("div", {"class": "subContentsInner"}):
			temp = unicode(p)
			if temp != "entryBottom" and not "google_ad_section" in temp:
				new_post.content += temp
		
		new_post.id = wp.call(posts.NewPost(new_post))
		
		# Publish the post
		new_post.post_status = 'publish'
		wp.call(posts.EditPost(new_post.id, new_post))


# Post sonymusic posts to Wordpress
def post_to_wp_sonymusic(post_content, cred):
	# Set up wordpress to accept posts from script
	wp = Client(cred[0], cred[1], cred[2])
	
	for entry in post_content:
		new_post = WordPressPost()
		new_post.title = unicode(entry[0].find_all("p")[0].contents[0])
		
		new_post.content = u"***Begin Original Content Here***\u000D"
		new_post.content += u"Posted on: " + entry[0].find("p", {"class": "infoDate"}).contents[0] + u"\u000D"
		new_post.content += u"<a href=\u0022" + entry[1] + u"\u0022>See original post</a>\u000D"
		
		for p in entry[0].find("div", {"id": "infoArticle"}):
			temp = unicode(p)
			new_post.content += temp
	
		new_post.id = wp.call(posts.NewPost(new_post))

		# Publish the post
		new_post.post_status = 'publish'
		wp.call(posts.EditPost(new_post.id, new_post))



if __name__ == "__main__":
	pass
