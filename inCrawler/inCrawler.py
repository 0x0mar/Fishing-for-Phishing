import re, urllib, random, webbrowser, urllib2, sys
import json

#phishListParsed = []
#json_list = open('seed.json', 'rb')
#phishList = json.load(json_list)
#for row in phishList:
#	phishListParsed.append(row['url'])

urlBank = ['http://www.solarmovie.eu','http://www.weather.com']
phishBank = []
done = 0

while done == 0:
	if len(urlBank) > 10000:
		urlBank [:100]
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl = urlBank.pop(x)
	try: 
		if len(phishBank) >= 3:
			phishList = open('output.txt', 'w')
			done = 1
			for i in phishBank:	
				phishList.write("%s \n" % i)
			phishList.close()

		for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(crawl).read(200000), re.I):
			z = re.match('http://' , i)
			if z:
				urlBank.append(i)
				reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + i
				response = urllib2.urlopen(reqURL).getcode()
				if (response==200):
					print ("FOUND %s" %i)
					phishBank += i
			
	except Exception as e:
		print ("Broken link to %s" %i)	
		print (type(e))
		print (e.args)		
			
print ("finished!")

