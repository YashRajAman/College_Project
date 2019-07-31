#importing needed library and classes

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.servers import ThreadedFTPServer
import threading
import tkinter as tk
from tkinter import messagebox
import MySQLdb as sql
from functools import partial





ip =""
port = 0

def testprint():
    ip = ipentry.get()
    print(ip)
    #print(portentry.get())


#user authentication form database
conn = sql.connect(host='localhost', database='ServerUsers', user='serveruser', password='serveradmin')
cursor = conn.cursor()
cursor.execute('select * from ActiveServerUser')
rows = cursor.fetchall()
print("Allowed users with password.")
for row in rows:
    print(row)


authorizer = DummyAuthorizer()
#Adding users from database
for row in rows:
    authorizer.add_user(row[0], row[1], "/home/mahaadev/Desktop/programing", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer
#closing database connection
conn.close()

def createserver(ip, port):
    try:
        server = FTPServer((ip, port), handler)
        print(ip + str(port))
        messagebox.showwarning("Server says: ", "Server is online")
        t = threading.thread(target=server.serve_forever)
        while(True):
            t.start()
        #server.serve_forever()
    except:
        print("Server Creation Failed")
        messagebox.showerror("Server Creatio Error!!!", "Can't create server :( \nCheck IP and Port !")


#gui creation for the server 
def call_result(label_result, n1, n2):  
    ip = (n1.get())  
    port = int((n2.get()))
    print("Got Ip and port address.")
    print(ip+ str(port))
    return  [ip, port]
def getandcreate():
    print("Calling server creation functions")
    address = call_result()
    createserver(address[0], address[1])
    print("Called server Creation")
   




root = tk.Tk()  
#root.geometry('400x200+100+200')  
  
root.title('FTP Server ....!!!')  
   
number1 = tk.StringVar()  
number2 = tk.StringVar()  
  
labelNum1 = tk.Label(root, text="Input IP Address   :").grid(row=1, column=0)  
  
labelNum2 = tk.Label(root, text="Input Port Address :").grid(row=2, column=0)  
  
labelResult = tk.Label(root)  
  
labelResult.grid(row=7, column=2)  
  
entryNum1 = tk.Entry(root, textvariable=number1).grid(row=1, column=2)  
  
entryNum2 = tk.Entry(root, textvariable=number2).grid(row=2, column=2)  
  
call_result = partial(call_result, labelResult, number1, number2)  
  
buttonCal = tk.Button(root, text="Create Server ", command=getandcreate).grid(row=3, column=0)  

root.mainloop() 

