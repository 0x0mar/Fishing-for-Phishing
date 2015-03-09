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

def emailSeed (db):
	#establish cursor, update tld data
	cursor = db.cursor()
	update_tld_names()
	domain = ""
	spamMsgs={}

	try:	
		#get the whitelist from the sql server
		execString = ("SELECT Domain FROM WhiteList;") 
		cursor.execute(execString)
		wl = list(cursor)
	except:
		print ("Couldn't read whitelist")
		
	try:
		#use a file user.json in this directory to log into Gmail and pull down spam
		CLIENT_SECRET_FILE = 'user.json'
		OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
		STORAGE = Storage('gmail.storage')
		flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
		http = httplib2.Http()
		credentials = STORAGE.get()
		if credentials is None or credentials.invalid:
			credentials = run(flow, STORAGE, http=http)
		http = credentials.authorize(http)
		gmail_service = build('gmail', 'v1', http=http)
		spamMsgs = gmail_service.users().messages().list(userId='me', labelIds='SPAM').execute()
		execString = ""
		i=0
		
	except Exception as e: 
		print ("Unable to access spam email. You need user.json gmail credentials in this directory.")
		print (type(e))
		print (e.args)
		
	for spam in spamMsgs['messages']:
		i = i+1
		try:
			#get messages
			messageId =(spam['id'])
			message = gmail_service.users().messages().get(id=messageId, userId='me').execute()
			stringe = (message['payload']['body'])
				
			#add each message part to the database
			for part in message['payload']['parts']:
				print part
				content = part['body']['data']
				content = base64.urlsafe_b64decode(content.encode('ascii'))
				for url in re.findall('''http["'](.[^"']+)["']''', content):
					try:
						#set bad if in whitelist
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
				execString = ("INSERT IGNORE INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('0', '%s', '%i', '%s', 'email');" % (content, i, str(messageId))) 
				cursor.execute(execString)
				db.commit()
		except Exception as e:
			print ("Failed to load email with SQL query: %s" %execString)	
			print (type(e))
			print (e.args)
	
	db.close()

