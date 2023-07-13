# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 19:36:26 2023

@author: Swagster

Instant Messenger App Project : Server Side
"""

import socket
import selectors
import types

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="34SKlsa12",
  database="text_server"
)
mycursor = mydb.cursor()

'''def confirmUser(name, password):
    mycursor.execute("select * from user where user.name like {} AND user.password like {}".format(name, password ) )
    if mycursor[0][0] == name and mycursor[0][1] == password:
        
    pass
'''
HOST = "127.0.0.1" # loop back interface, so only my machine will connect to it
CLIENT_COUNT = 10
MAX_BYTE = 1024
SAFEWORD = b"/close"
PORT = 6001

SELECTOR = selectors.DefaultSelector();

LISTEN_SOCKET = socket.socket( socket.AF_INET, socket.SOCK_STREAM );
LISTEN_SOCKET.bind( (HOST, PORT) );

print("Host IP : {}".format(HOST) )
print("Port Number : {}".format(PORT) )
print("constants initialized")

LISTEN_SOCKET.listen();
LISTEN_SOCKET.setblocking(False)

print("Ready!")
#time.sleep(10)
#LISTEN_SOCKET.close()

SELECTOR.register( LISTEN_SOCKET, selectors.EVENT_READ, data=None )

listOfSockets = []
confirmedSockets = []

try:
    while True:
        events = SELECTOR.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                #accept_wrapper(key.fileobj)
                print("New User")
                sockManage = key.fileobj
                cnxn, address = sockManage.accept()
                print("Connection from Address : {}".format(address) )
                cnxn.setblocking(False)
                
                listOfSockets.append( cnxn )
                confirmedSockets.append( False )
                
                data = types.SimpleNamespace(addr=address, inb=b"", outb=b"")
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                SELECTOR.register( cnxn, events, data=data )
                
            else:
                #print("Client Action : Processing")
                sockManage = key.fileobj
                data = key.data
                
                if mask & selectors.EVENT_READ:
                    getData = sockManage.recv(MAX_BYTE)
                    
                    if getData != "":
                        data.outb = data.outb + getData
                    if getData == "" or getData == SAFEWORD:
                        print(f"Closing connection to {data.addr}")
                        SELECTOR.unregister(sockManage)
                        sockManage.close()
                        
                if mask & selectors.EVENT_WRITE:
                    if data.outb != b'':
                        #print(f"Echoing {data.outb!r} to {data.addr}")
                        print(data.outb)
                        sendInfo =  data.outb
                        
                        #selectors.select()
                        for i in listOfSockets:
                            #try:
                            i.send(b"\n>> " + data.outb)
                            #except OSError or ConnectionResetError:
                                #break
                        #sent = sockManage.send(data.outb) 
                        #data.outb = data.outb[sent:]
                        data.outb = b''
                    
                #service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    LISTEN_SOCKET.close()
    SELECTOR.close()

