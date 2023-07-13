# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 21:51:16 2023

@author: Swagster
    
Instant Messenger App Project : Client Side
"""

import tkinter
import socket
import sys


#LOOP = True

def sendContents():
    out = entry.get()
    s.sendall( bytes( out, 'utf-8' ) )
    if out == "/close":
        root.destroy()
        sys.exit()
    data = s.recv(1024)
    print(f"Received {data!r}")
    
    #txtBox.insert("1.0", data)
    
def looper():
    #while 1:
        #print("testing")
        
        root.after(1, looper)
        try:
            #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #s.setblocking(False)
                
                while True:
                    #print("Waiting for Messages")
                    data = s.recv(1024)
                    print( "Message Recieved : {}".format(data) )
                    txtBox.insert("1.0", data)
                    
               #LOOP = False
               
        except KeyboardInterrupt: 
            print("killed")
            #break
        except BlockingIOError:
            pass
        

HOST = "127.0.0.1"
PORT = 6001

root = tkinter.Tk()
root.title("Instant Messenger")
root.geometry("500x500")

txtBox = tkinter.Text()
entry = tkinter.Entry()
sendButt = tkinter.Button(text="Send", command=sendContents)

txtBox.pack()
entry.pack()
sendButt.pack()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.connect_ex((HOST, PORT))
print("Connection Established")
#s.settimeout(0)
s.setblocking(False)

root.after(0, looper)
root.mainloop()









