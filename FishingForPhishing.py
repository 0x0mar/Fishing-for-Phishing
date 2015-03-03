import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
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
		outLinks = []
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
							execString = ("INSERT INTO outboundLinks (Lvl, Domain, domainTo, URL, URLto, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', 'false', '%i');" % ((i+1), domain, domainTo, url, k, bad))
							cursor.execute(execString)
							
							#update the record, we've crawled this link
							execString = ("UPDATE IGNORE outboundLinks SET Crawled=0 WHERE domain= '%s' AND domainTo='%s';" % (domain, domainTo))
							cursor.execute(execString)
							db.commit()
							
					except Exception as e:
						#couldn't handle this link, change crawled to 2 to take it out of circulation
						print ("Couldn't add " + k + " error: " )
						print e
						execString = ("UPDATE outboundLinks SET Crawled=2 WHERE domain= '%s' AND domainTo='%s';" % (domain, domainTo))
						cursor.execute(execString)

				content=db.escape_string(content)
				execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('%i', '%s', '%s', '%s', 'crawl');" % ((i+1), content, domain, url)) 
				cursor.execute(execString)

				db.commit()
			except Exception as e:
				print ("Couldn't crawl: %s \n" %url)	
				print (type(e))
				print (e.args)
	db.close()
	
if __name__ == '__main__':
	crawl()
	
