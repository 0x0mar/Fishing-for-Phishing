import re, urllib, random, webbrowser, urllib2, sys
import json
import MySQLdb
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()

#phishListParsed = []
#json_list = open('seed.json', 'rb')
#phishList = json.load(json_list)
#for row in phishList:
#	phishListParsed.append(row['url'])

db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
cursor = db.cursor()

urlBank = ['http://www.solarmovie.eu','http://www.fullmovie2k.com/','http://www.tricksforums.com/2014/08/best-5-free-movie-streaming-site-to.html','http://www.reelwavs.com/mstop25/','http://www.tamilo.com/','http://lasvegasfreemovies.com/','http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=175&cad=rja&uact=8&ved=0CDYQFjAEOKoB&url=http%3A%2F%2Fwww.xnxx.com%2Fhome%2F5%2F&ei=AtjJVKujAoHQgwS5l4DADw&usg=AFQjCNETanxkj0brrevC6jyK8Y_Kwmfk1A&sig2=N9EMvj2PG76h1Yc3h5AuZQ&bvm=bv.84607526,d.eXY','http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=208&cad=rja&uact=8&ved=0CEgQFjAHOMgB&url=http%3A%2F%2Fwww.gonzoxxxmovies.com%2F&ei=LNjJVOGKDI_ggwThkoTABw&usg=AFQjCNHrkb6c3LgwrNN1CWsJz-C5pWrFEw&sig2=rkwyiaHUchgikWEUIeFeVQ&bvm=bv.84607526,d.eXY', 'http://www.dmoz.org/World/Bulgarian/','http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Chinese_Simplified/','http://www.internet-directory.com/','http://www.botid.org/','http://www.joeant.com/', 'https://kickass.so/', 'http://www.popularart.be/?option=com_k2&view=itemlist&task=user&id=1110', 'http://winit.intouchweekly.com/']
phishBank = []
done = 0
domDict = {}

while done == 0:
	if len(urlBank) > 10000:
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
				try:
					z = (re.match('http://' , i) or re.match('//' , i))
					y = re.match('/' , i)
					if (y):
						i = (("/").join((re.split("/", url)))+i)			
					if z or y:
						domainTo= (get_tld(i, fail_silently=True))
						urlBank.append(i)
						reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + i
						response = urllib2.urlopen(reqURL).getcode()
						if (response==200):
							print ("FOUND %s" %i)
							execString = ("INSERT INTO seed (Domain, URL, URLSource, Crawled) VALUES ('%s', '%s', 'crawl', '0');" % (domain, i)) 
							cursor.execute(execString)
							execString = ("INSERT INTO inboundLinks (Domain, domainTo, URL, URLto, CopySource, Crawled) VALUES ('%s','%s', '%s', '%s', 'crawl', '0');" % (domain, domainTo, url, i)) 
							cursor.execute(execString)
						else:
							execString = ("INSERT INTO safeSeed (Domain, URL, URLSource, Crawled) VALUES ('%s', '%s', 'crawl', '0');" % (domain, i)) 
							cursor.execute(execString)
				except Exception as e:
					print ("Couldn't add %s" %i)
					print e	
	except Exception as e:
		print ("Broken link to %s" %i)	
		print (type(e))
		print (e.args)		
			
print ("finished!")

