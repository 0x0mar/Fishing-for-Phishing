import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
reload(sys)
sys.setdefaultencoding('utf8')

def write(db):
	cursor = db.cursor()
	try:
		#open a local whitelist file and store those in database
		with open('wl.csv', 'rb') as csvfile:
			wlreader = csv.reader(csvfile, delimiter=',')
			for row in wlreader:
				fixedRow = (row[1].split("/")[0])
				execString = ("INSERT IGNORE INTO WhiteList(Domain, Rank) VALUES ('%s', '%s');" %(fixedRow, row[0])) 
				cursor.execute(execString)
		db.commit()
		db.close()
		
	except:
		print ("Unable to load whitelist into database")
	
