
#!/usr/bin/python

import httplib2
import base64
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

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
threads = gmail_service.users().threads().list(userId='me').execute()
labels = gmail_service.users().labels().list(userId='me').execute()
spams = gmail_service.users().messages().list(userId='me', labelIds='SPAM').execute()
i =0 
if spams['messages']:
  for spam in spams['messages']:
	messageId =(spams['messages'][i]['id'])
	message = gmail_service.users().messages().get(id=messageId, userId='me').execute()
	stringe = (message['payload']['body'])
	if (stringe.get('data',"")):
			stringd = base64.urlsafe_b64decode(stringe['data'].encode('ascii'))
			print stringd
	print "************************* \n"
	i+=1
    


    

