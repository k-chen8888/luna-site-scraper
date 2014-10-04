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
# Gives a list of files that were created
#	List also includes 'n' (new) or 'e' (edited)
def json_dump(content, source, loc):
	try:
		os.chdir(loc)
	except OSError:
		print "nope"
		return []
	
	files = []
	
	# Each entry has either been indexed already or needs to be indexed
	for entry in content:
		new_file_name = unicode(source) + u"-"
		dict_content = {}
		
		# Use different tools depending on source
		if source == "ameblo":
			# Clean up date and encorporate into file
			for x in [i for i in entry[0].find("span", {"class": "date"}).contents[0].strip('- :') if i.isdigit()]:
				new_file_name += unicode(x)
				
			# Convert to dictionary before feeding to json loader
			dict_content = extract_dict_ameblo(entry[0])
		
		elif source == "sonymusic":
			for x in [i for i in entry[0].find("p", {"class": "infoDate"}).contents[0].strip('- :') if i.isdigit()]:
				new_file_name += unicode(x)
			
			dict_content = extract_dict_sonymusic(entry[0])
			
		new_file_name += ".txt"
		new_file_name = new_file_name.decode('ascii')
		
		# Dump to JSON
		json_temp = json.dumps(dict_content, ensure_ascii=False, indent=4, sort_keys=True)
		
		if not os.path.isfile(new_file_name):
			with open(new_file_name, 'w') as outfile:
				outfile.write(json_temp)
				outfile.close()
			files.append([new_file_name, 'n'])
		else:
			# Check contents of file and replace as needed
			# Add to list if changes made
			with open(new_file_name, 'r+') as old_json:
				if check_contents(old_json, json_temp):
					files.append([new_file_name, 'e'])
				else:
					files.append([new_file_name, 'o'])
					
				old_json.close()
	
	for f in files:
		print f
	
	os.chdir("..")
	
	return files


# Checks if content matches existing content
# On pure matches, reject scraped content
# On changes, replace
# Returns true if contents replaced
def check_contents(old_content, new_content):
	old_temp = json.dumps(json.load(old_content), ensure_ascii=False, indent=4, sort_keys=True)

	if old_temp != new_content.decode('utf-8'):
		# Erase file
		old_content.seek(0)
		old_content.truncate()
		
		# Write new content
		old_content.write(new_content)
		
		return True
		
	# No changes if content matches
	else:
		print "match"
		return False


# Converts BeautifulSoup for ameblo to a dictionary
def extract_dict_ameblo(entry):
	dict_out = {}
	
	dict_out['title'] = unicode(entry.find("h3").find("a").contents[0]).encode('utf-8')
	dict_out['date'] = unicode(entry.find("span", {"class": "date"}).contents[0]).encode('utf-8')
	dict_out['p'] = {}
	
	# Get all elements that have content in them
	counter = 0
	for p in entry.findAll("p"):
		if counter < 10:
			name = 'line_0' + str(counter)
		else:
			name = 'line_' + str(counter)
		
		dict_out['p'][name] = unicode(p.text).encode('utf-8')
		counter = counter + 1
	
	return dict_out


# Converts BeautifulSoup for sonymusic to a dictionary
def extract_dict_sonymusic(entry):
	dict_out = {}
	
	dict_out['title'] = unicode(entry.find("p", {"id": "infoCaption"}).contents[0]).encode('utf-8')
	dict_out['date'] = unicode(entry.find("p", {"class": "infoDate"}).contents[0]).encode('utf-8')
	dict_out['p'] = {}
	
	# Get all elements that have content in them
	counter = 0
	for e in entry.findChildren():
		if e.name != "br":
			if counter < 10:
				name = 'line_0' + str(counter)
			else:
				name = 'line_' + str(counter)
			
			dict_out['p'][name] = unicode(e.text).encode('utf-8')
			counter = counter + 1
	
	return dict_out



if __name__ == "__main__":
	pass
