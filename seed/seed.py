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

db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
cursor = db.cursor()

json_seed = open('seed.json', 'rb')
seedx = json.load(json_seed)

wl = []
with open('wl.csv', 'rb') as csvfile:
	wlreader = csv.reader(csvfile, delimiter=',')
	for row in wlreader:
		string=(row[1].split("/"))[0]
		wl.append(string)
		
for row in seedx:
	url=row['url']
	domain = (url.split("/"))[2]
	try:
		execString = ("INSERT IGNORE INTO seed (Domain, URL, URLSource, crawled) VALUES ('%s', '%s', 'list', '0');" % (domain, url))
		cursor.execute(execString)
		db.commit()
	except:
		print("Broken link")

CLIENT_SECRET_FILE = '/home/jcbraun/Downloads/user.json'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
STORAGE = Storage('gmail.storage')
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)
http = credentials.authorize(http)
gmail_service = build('gmail', 'v1', http=http)
spams = gmail_service.users().messages().list(userId='me', labelIds='SPAM').execute()
execString = "" 
for spam in spams['messages']:
	try:
		messageId =(spam['id'])
		message = gmail_service.users().messages().get(id=messageId, userId='me').execute()
		stringe = (message['payload']['body'])	
		stringd = base64.urlsafe_b64decode(stringe.encode('ascii'))
		for url in re.findall('''http["'](.[^"']+)["']''', stringd):
			domainTo = (url.split("/"))[2]
			if ((domain + "/") in wl):
				print ("Whitelisted \n")
				bad = 0
			else:
				bad =1
			execString = ("INSERT IGNORE INTO seed (Domain, URL, URLSource, crawled) VALUES ('%s', '%s', 'list', 0);" % (domain, url))
			cursor.execute(execString)
		stringd=db.escape_string(stringd)
		execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('0', '%s', 'EMAIL', '%s', 'email');" % (stringd, str(messageId))) 
		cursor.execute(execString)
		db.commit()
	except Exception as e:
		print ("Broke: %s" %execString)	
		print (type(e))
		print (e.args)
db.close()

