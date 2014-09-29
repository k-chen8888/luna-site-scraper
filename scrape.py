# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

# Allow command line arguments through sys
import sys

# Use modules
from sites import scrape_tools, do_not_repeat
from post import wp_writer


# Get the title and content of every post and put it in an array
def get_all_content(cred):
	wp = Client(cred[0], cred[1], cred[2])
	return [ [x.title, x.content] for x in wp.call(posts.GetPosts()) ]



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
			post_to_wp_ameblo(get_post_list_ameblo(url), wp_cred)
		elif 'sonymusic.co.jp' in url:
			post_to_wp_sonymusic(get_post_list_sonymusic(url), wp_cred)
		else:
			print "Malformed file"
