import re, urllib, random, webbrowser, urllib2, sys
import json
import mechanize

#phishListParsed = []
#json_list = open('seed.json', 'rb')
#phishList = json.load(json_list)
#for row in phishList:
#	phishListParsed.append(row['url'])

phishBank = []
done = 0
 
qe="sign+up+email+list" 
counter = 0
 
for i in range(0,9):
	br = mechanize.Browser()
	google_url = br.open("https://www.google.com/search?q=" + qe + "&amp;amp;start=" + str(counter))
	search_keyword = google_url.read()
	for link in br.links():
		urlBank += link
	counter+=10


while done == 0:
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl = urlBank.pop(x)
	try: 
		br = mechanize.Browser()
		br.addheaders = [("User-agent","Mozilla/5.0")] #our identity in the web
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

