import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	db = MySQLdb.connect(host='127.0.0.1',db='jcbraunDB',user='root',passwd='3312crystal')
	cursor = db.cursor()
	with open('wl.csv', 'rb') as csvfile:
		wlreader = csv.reader(csvfile, delimiter=',')
		for row in wlreader:
			fixedRow = (row[1].split("/")[0])
			execString = ("INSERT INTO WhiteList(Domain, Rank) VALUES %s %s;" %(fixedRow, row[0])) 
			cursor.execute(execString)
	db.commit()
	db.close()
	
if __name__ == '__main__':
	crawl()
	
