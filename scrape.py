# Wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts

# Allow command line arguments through sys
import sys

# Use modules
from sites import scrape_tools, json_dump
from post import wp_writer


# Get the title and content of every post and put it in an array
def get_all_content(cred):
	wp = Client(cred[0], cred[1], cred[2])
	return [ [x.title, x.content] for x in wp.call(posts.GetPosts()) ]


# Removes information that will not be dumped to a post
# @content is a list
# 	0: BeautifulSoup object
# 	1: Origin URL
# @source is a string with name of content provider
# @loc is storage location of all json files
def clean_content(content, source, loc):
	test = json_dump.json_dump(content, source, loc)
	
	print test
	
	valid_content = []
	
	for t, x in zip(test, content):
		if t[1] == 'n':
			valid_content.append(x)
	
	return valid_content


if __name__ == "__main__":
	try:
		urlf = open(sys.argv[1], 'r')
		urls = [x.strip() for x in urlf]
		
		wp_info = open(sys.argv[2], 'r')
		wp_cred = [x.strip() for x in wp_info]
		
		if len(urls) != 0 and len(wp_cred) == 3:
			# Get the actual content and dump it to Wordpress
			for url in urls:
				if 'ameblo.jp' in url:
					wp_writer.post_to_wp_ameblo(clean_content(scrape_tools.get_post_list_ameblo(url), "ameblo", "json"), wp_cred)
				elif 'sonymusic.co.jp' in url:
					wp_writer.post_to_wp_sonymusic(clean_content(scrape_tools.get_post_list_sonymusic(url), "sonymusic", "json"), wp_cred)
				else:
					print "Malformed file"
		else:
			print "Files not properly formatted or there was not enough information to work with"
		
		# Close files
		urlf.close()
		wp_info.close()
		
	except IOError:
		print "Not a file"
