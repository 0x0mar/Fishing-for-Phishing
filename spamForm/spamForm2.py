import re, urllib, random, webbrowser, urllib2, sys
import json
import mechanize
from pygoogle import pygoogle


#phishListParsed = []
#json_list = open('seed.json', 'rb')
#phishList = json.load(json_list)
#for row in phishList:
#	phishListParsed.append(row['url'])

phishBank = []
done = 0
try:
	g = pygoogle('sign up email list')
	br = mechanize.Browser()
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False) 
	response = br.open(crawl)
	print crawl
	br.form = list(br.forms())[0]
	for control in br.form.controls:
		if control.type == "text":  # means it's class ClientForm.TextControl
			control.value = "phishing4f@gmail.com"
		response = br.submit()
		print response
		print("SUCCCCCCESSSSSSSSS")
			
except Exception as e:
	print ("Broken link to %s" %crawl)	
	print (type(e))
	print (e.args)		
			
print ("finished!")

