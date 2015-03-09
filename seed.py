import json
import MySQLdb
import httplib2
import csv
import base64
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
import re
from tld import get_tld
from tld.utils import update_tld_names

def seed (db):
	#establish cursor, update tld data
	cursor = db.cursor()
	update_tld_names()
	domain = ""
	#insert sites from seed and safeSeed csv files
	with open('seed.csv', 'rb') as csvfile:
		seedReader = csv.reader(csvfile, delimiter=',')
		for link in seedReader:
			link = link[0]
			if get_tld(link, fail_silently=True) != None:
				print "ADDING %s TO SPAM SEED... \n" % link
				domain = get_tld(link, fail_silently=True)
			try:
				execString = ("INSERT IGNORE INTO seed(Domain, URL, URLSource, Crawled) VALUES ('%s', '%s', 'list', '0');" %(domain, link)) 
				cursor.execute(execString)
				db.commit()
			except:
				print ("FAILED TO EXECUTE SQL QUERY: %s" %execString)
				
	with open('safeSeed.csv', 'rb') as csvfile:
		seedReader = csv.reader(csvfile, delimiter=',')
		for link in seedReader:
			link = link[0]
			if get_tld(link, fail_silently=True) != None:
				print "ADDING %s TO SAFE SEED... \n" % link
				domain = get_tld(link, fail_silently=True)
			try:
				execString = ("INSERT IGNORE INTO safeSeed(Domain, URL, URLSource, Crawled) VALUES ('%s', '%s', 'list', '0');" %(domain, link)) 
				cursor.execute(execString)
				db.commit()
			except:
				print ("FAILED TO EXECUTE SQL QUERY: %s" %execString)			
		
	try:	
		#get the whitelist from the sql server
		execString = ("SELECT Domain FROM WhiteList;") 
		cursor.execute(execString)
		wl = list(cursor)
		
		#use a file user.json in this directory to log into Gmail and pull down spam
		flow = flow_from_clientsecrets('user.json', scope='https://www.googleapis.com/auth/gmail.readonly')
		http = httplib2.Http()
		credentials = 'gmail.storage'.get()
		if credentials is None or credentials.invalid:
		  credentials = run(flow, 'gmail.storage', http=http)
		http = credentials.authorize(http)
		gmail_service = build('gmail', 'v1', http=http)
		spamMsgs = gmail_service.users().messages().list(userId='me', labelIds='SPAM').execute()
		execString = "" 
		i=0
		
	except: 
		print ("Unable to read spam email. You need user.json gmail credentials in this directory.")
		
		for spam in spamMsgs['messages']:
			i = i+1
			try:
				print spam
				messageId =(spam['id'])
				message = gmail_service.users().messages().get(id=messageId, userId='me').execute()
				stringe = (message['payload']['body'])	
				for part in message['payload']['parts']:
					content = part['body']['data']
					content = base64.urlsafe_b64decode(content.encode('ascii'))
					for url in re.findall('''http["'](.[^"']+)["']''', content):
						try:
							domainTo = (url.split("/"))[2]
							if ((domain + "/") in wl):
								print ("Whitelisted \n")
								bad = 0
							else:
								bad =1
							execString = ("INSERT IGNORE INTO seed (Domain, URL, URLSource, crawled) VALUES ('%s', '%s', 'list', 0);" % (domain, url))
							cursor.execute(execString)
						except:
							print "Failed to add this piece of spam"
					content=db.escape_string(content)
					execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('0', '%s', '%i', '%s', 'email');" % (content, i, str(messageId))) 
					cursor.execute(execString)
					db.commit()
			except Exception as e:
				print ("Failed to load email: %s" %execString)	
				print (type(e))
				print (e.args)
		
	db.close()

