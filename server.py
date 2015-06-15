import socket
from Predict import SVMpredict, NBpredict, getContentPredict
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portNum = sys.argv[1]
try:
    server.bind(('',int(portNum)))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

server.listen(10)
 
def clientthread(openSocket):
    while True:
        try: 
            url = openSocket.recv(1024)
            if not url:
                break
            openSocket.send(str(getContentPredict(url)) + "\n")
        except: 
            openSocket.send("Unable to recover prediction \n")
    openSocket.close()
 
while True:
    try: 
        openSocket, addr = server.accept()
        start_new_thread(clientthread ,(openSocket,))
    except:
        print ("unable to open socket \n")
s.close()