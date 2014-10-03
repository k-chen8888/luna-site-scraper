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
		return []
	
	files = []
	
	# Each entry has either been indexed already or needs to be indexed
	for entry in content:
		new_file_name = unicode(source) + u"-"
		
		# Clean up date format
		for x in [i for i in entry.find("span", {"class": "date"}).contents[0].strip('- :') if i.isdigit()]:
			new_file_name += unicode(x)
		
		new_file_name += u".txt"
		
		json_temp = json.loads(str(entry))
		
		if not os.path.isfile(new_file_name):
			json.dump(json_temp, open(new_file_name, 'w'))
			files.append(new_file_name)
		else:
			# Check contents of file and replace as needed
			old_json = open(new_file_name, 'r+')
			
			# Add to list if changes made
			if check_contents(old_json, json_temp):
				files.append(new_file_name)
			
			old_json.close()
	
	return files


# Checks if content matches existing content
# On pure matches, reject scraped content
# On changes, replace
# Returns true if contents replaced
def check_contents(old_content, new_content):
	old_temp = json.loads(old_content)
	if cmp(old_temp, new_content) != 0:
		old_content.seek(0)
		old_content.truncate()
		json.dump(new_content, old_content)
		return true
	else:
		return false


if __name__ == "__main__":
	pass
