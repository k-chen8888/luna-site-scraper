import re
import json
import os
from bs4 import BeautifulSoup


# Dump content to json based on source
# 	Source is a string that identifies the location from which information was pulled
# Searches in the location given for that json 
# Location format should be "/dirname"
# Filenames are of form "source-date.txt"
# Processes information to find matches
def json_dump(content, source, loc):
	try:
		os.chdir(loc)
	except OSError:
		return
	
	# Each entry has either been indexed already or needs to be indexed
	for entry in content:
		new_file_name = unicode(source) + u"-"

		# Clean up date format
		for x in [i for i in entry.find("span", {"class": "date"}).contents[0].strip('- :') if i.isdigit()]:
			new_file_name += unicode(x)
		
		new_file_name += u".txt"

		if not os.path.isfile(new_file_name):
			json.dump(entry, open(new_file_name, 'w'))
		else:
			# Check contents of file and replace as needed



# Checks if content matches existing content
# On pure matches, reject scraped content
# On changes, replace
def do_not_repeat(old_content, new_content):
	pass
