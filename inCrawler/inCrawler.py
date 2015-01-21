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

urlBank = ['http://www.solarmovie.eu','http://www.weather.com', 'http://www.dmoz.org/World/Bulgarian/','http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Chinese_Simplified/','http://www.internet-directory.com/','http://www.botid.org/','http://www.joeant.com/', 'https://kickass.so/', 'http://www.popularart.be/?option=com_k2&view=itemlist&task=user&id=1110', 'http://winit.intouchweekly.com/']
phishBank = []
done = 0
domDict = {}

while done == 0:
	if len(urlBank) > 1000:
		urlBank = ['http://www.solarmovie.eu','http://www.weather.com', 'http://www.dmoz.org/World/Bulgarian/','http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Chinese_Simplified/','http://www.internet-directory.com/','http://www.botid.org/','http://www.joeant.com/', 'https://kickass.so/', 'http://www.popularart.be/?option=com_k2&view=itemlist&task=user&id=1110', 'http://winit.intouchweekly.com/']
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl = urlBank.pop(x)
	url= crawl
	domain = (url.split("/"))[2]
	if domDict.has_key(domain):
		print "Count is %s \n" %domDict[domain]
		domDict[domain] += 1
	else:
		domDict[domain] = 0
	try: 
		if domDict[domain] < 10:
			for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(crawl).read(200000), re.I):
				z = re.match('http://' , i)
				if z:
					urlBank.append(i)
					reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + i
					response = urllib2.urlopen(reqURL).getcode()
					if (response==200):
						print ("FOUND %s" %i)
						execString = ("INSERT INTO Seed (Domain, URL, URLSource, Crawled) VALUES ('%s', '%s', 'crawl', '0');" % (domain, i)) 
						cursor.execute(execString)
						execString = ("INSERT INTO inboundLinks (Domain, URL, URLto, CopySource) VALUES ('%s', '%s', '%s', 'crawl');" % (domain, url, i)) 
						cursor.execute(execString)
			
	except Exception as e:
		print ("Broken link to %s" %i)	
		print (type(e))
		print (e.args)		
			
print ("finished!")

