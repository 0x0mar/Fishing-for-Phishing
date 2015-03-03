import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
from seed import seed

update_tld_names()
reload(sys)
sys.setdefaultencoding('utf8')

def crawl():
	db = MySQLdb.connect(host='127.0.0.1',db='jcbraunDB',user='root',passwd='3312crystal')
	cursor = db.cursor()
	
	#get the whitelist from the sql server
	execString = ("SELECT Domain FROM WhiteList;") 
	cursor.execute(execString)
	wl = list(cursor)
	
	#make sure we've crawled the seed, then move out one level at a time
	i=0
	while (True):
		if (i==0):
			execString = ("SELECT URL, Domain FROM seed WHERE crawled=0;") 
			cursor.execute(execString)
			seedx = cursor.fetchall()
		else:
			execString = ("SELECT URLTo FROM outboundLinks WHERE lvl=%i AND toSpam=1 AND crawled=0;" % (i)) 
			cursor.execute(execString)
			seedx = cursor.fetchall()

		for row in seedx:
			try:
				url = row[0]
				domain = get_tld(url, fail_silently=True)
				content = urllib2.urlopen(url, timeout=3).read(200000)
				for k in re.findall('''href=["'](.[^"']+)["']''', content):
					try:
						print k
						z = ((re.match('http://' , k) is not None) or (re.match('//' , k) is not None))
						y = re.match('/' , k)
						if (y):
							k = (("/").join((re.split("/", url)))+k)			
						if z or y:
							domainTo = (get_tld(k, fail_silently=True))
							print "Adding link to: %s \n" %k
							if (domainTo in wl):
								print ("Whitelisted \n")
								bad = 0
							else:
								bad =1
							
							#found a link, insert it into outboundLinks
							execString = ("INSERT IGNORE INTO outboundLinks (Lvl, Domain, domainTo, URL, URLto, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', 'false', '%i');" % ((i+1), domain, domainTo, url, k, bad))
							cursor.execute(execString)
							
							#update the record, we've crawled this link
							execString = ("UPDATE IGNORE outboundLinks SET Crawled=0 WHERE domain= '%s' AND domainTo='%s';" % (domain, domainTo))
							cursor.execute(execString)
							db.commit()
							
					except Exception as e:
						#couldn't handle this link, change crawled to 2 to take it out of circulation
						print ("Couldn't add " + k + " error: " )
						print e
						execString = ("UPDATE IGNORE outboundLinks SET Crawled=2 WHERE domain= '%s' AND domainTo='%s';" % (domain, domainTo))
						cursor.execute(execString)

				content=db.escape_string(content)
				execString = ("INSERT IGNORE INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('%i', '%s', '%s', '%s', 'crawl');" % ((i+1), content, domain, url)) 
				cursor.execute(execString)

				db.commit()
			except Exception as e:
				print ("Couldn't crawl: %s \n" %url)	
				print (type(e))
				print (e.args)
	db.close()

def safeCrawl():
	i=0
	db = MySQLdb.connect(host='127.0.0.1',db='jcbraunDB',user='root',passwd='3312crystal')
	cursor = db.cursor()
	while (True):
		if (i==0):
			execString = ("SELECT URL, Domain FROM safeSeed WHERE crawled=0;") 
			cursor.execute(execString)
			seedx = cursor.fetchall()
		else:
			execString = ("SELECT URLTo FROM safeOutboundLinks WHERE lvl=%i AND crawled=0;" % (i)) 
			cursor.execute(execString)
			seedx = cursor.fetchall()
			
		for row in seedx:
			try:
				url = row[0]
				domain = get_tld(url, fail_silently=True)
				content = urllib2.urlopen(url, timeout=3).read(2000000)
				for k in re.findall('''href=["'](.[^"']+)["']''', content):
					try:	
						print "k: " + k		
						z = ((re.match('http://' , k) is not None) or (re.match('//' , k) is not None))
						y = re.match('/' , k)
						if (y is not None):
							k = (("/").join((re.split("/", url)))+k)
							print ("y")			
						if z or y:
							domainTo = (get_tld(k, fail_silently=True))
							print "domainTo is: %s" %domainTo
							reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + k
							response = urllib2.urlopen(reqURL).getcode()
							if (response==200):
								print ("Found dangerous site \n")
								execString = ("INSERT IGNORE INTO inboundLinks (Domain, domainTo, URL, URLto, Crawled) VALUES ('%s', '%s', '%s', '%s', 'false');" % (domain, domainTo, url, k))
								cursor.execute(execString)
							else:
								execString = ("INSERT IGNORE INTO safeOutboundLinks (Lvl, Domain, domainTo, URL, URLto, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', '0', '1');" % ((n+1), domain, domainTo, url, k))
								cursor.execute(execString)
								print("adding %s" %k)
							db.commit()	
					except Exception as e:
						print ("Couldn't add " + k + " error: " )
						print e
				bank = open('notspam/%dLVL%d.txt' %(i,n), 'w')
				bank.write (content)
				content=db.escape_string(content)
				execString = ("INSERT IGNORE INTO safeContent (Lvl, Content, Domain, URL, CopySource) VALUES ('%i', '%s', '%s', '%s', 'crawl');" % ((n+1), content, domain, url)) 
				cursor.execute(execString)
				print url + " success! \n"
				bank.close()
				
			except Exception as e:
				print ("Broken link to %s" %url)	
				print (type(e))
				print (e.args)
	db.commit()
	db.close()
	
if __name__ == '__main__':
	if sys.argv[1]=="crawl":
		print ("CRAWLING SPAM... \n")
		crawl()
	elif sys.argv[1]=="safecrawl":
		print ("CRAWLING SAFE LINKS... \n")
		safeCrawl()
	elif sys.argv[1]=="seed":
		print ("UPDATING SEED... \n")
		seed()
	