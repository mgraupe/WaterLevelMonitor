import requests
import xml.etree.ElementTree as ET

url = "http://www.infoclimat.fr/public-api/gfs/xml?_ll=48.85341,2.3488&_auth=ABoFEgB%2BBCZQfVBnA3VXflQ8BjMPeQYhVioAY1s%2BB3pROgRlB2dQNlI8B3oFKlBmWHUHZAswAzMBalIqDnxRMABqBWkAawRjUD9QNQMsV3xUegZnDy8GIVY9AG5bKAdnUSwEYQdhUDBSIwdnBTRQZVh0B3gLNQM%2BAWtSNw5mUTsAYwVnAGUEYlAgUC0DNlc2VDIGMg8wBj9WMQBvWzEHNVFnBGkHN1A3UiMHYAUxUGZYYgdjCzUDOgFkUioOfFFLABAFfAAjBCRQalB0Ay5XNlQ5BjI%3D&_c=5ba9a92a4f45fe915fb86afa9c45c7ff"
response = requests.get(url)

with open('infoclimat.xml', 'wb') as file:
	file.write(response.content)
file.close()

tree = ET.parse('infoclimat.xml')
root = tree.getroot()
for child in root: 
	print(child.tag,child.attrib) 
	if child.tag=='echeance':
		for subchild in child:
			#print(subchild.tag,subchild.attrib) 
			if subchild.tag=='pluie':
				print(subchild.text)
				for subsubchild in subchild:
					print(subsubchild.tag,subsubchild.attrib) 
