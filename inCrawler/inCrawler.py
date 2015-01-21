import re, urllib, random, webbrowser, urllib2, sys
import json
import MySQLdb

#phishListParsed = []
#json_list = open('seed.json', 'rb')
#phishList = json.load(json_list)
#for row in phishList:
#	phishListParsed.append(row['url'])

db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
cursor = db.cursor()

urlBank = ['http://www.solarmovie.eu','http://www.weather.com', 'https://kickass.so/', 'http://www.popularart.be/?option=com_k2&view=itemlist&task=user&id=1110']
phishBank = []
done = 0

while done == 0:
	if len(urlBank) > 1000:
		urlBank = ['http://www.solarmovie.eu','http://www.weather.com', 'https://kickass.so/', 'http://www.popularart.be/?option=com_k2&view=itemlist&task=user&id=1110']
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl = urlBank.pop(x)
	try: 
		for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(crawl).read(200000), re.I):
			z = re.match('http://' , i)
			if z:
				urlBank.append(i)
				reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + i
				response = urllib2.urlopen(reqURL).getcode()
				if (response==200):
					print ("FOUND %s" %i)
					phishBank += i
					execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('0', '%s', '%s', '%s', 'crawl');" % (content, domain, url)) 
					cursor.execute(execString)
			
	except Exception as e:
		print ("Broken link to %s" %i)	
		print (type(e))
		print (e.args)		
			
print ("finished!")

