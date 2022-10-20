# first of all import the socket library
import socket
import threading
from _thread import *
import random
import math
import pickle

# create a socket object
s = socket.socket()  # socket created
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 1234

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))

# put the socket into listening mode
s.listen(1)
print("Waiting for Connections")

ThreadCount = 0

def egcd(e,r):            # to find e gcd check
    while(r!=0):
        e,r=r,e%r
    return e

# Extended Euclidean Algorithm
def eea(a,b):
    if(a%b==0):
        return(b,0,1)
    else:
        gcd,s,t = eea(b,a%b)
        s = s-((a//b) * t)
        return(gcd,t,s)
        
def mult_inv(e,r):        # to find d multiplicative inverse
    gcd,s,_=eea(e,r)
    if(gcd!=1):
        return None
    else:
        return s%r

def make_key(p,q):
    n=p*q
    r= (p-1)*(q-1)    # Euler Totient
    e,d=0,0
    
#     find e st. e and r are coprime
    for i in range(1,1000):
        if(egcd(i,r)==1):    e=i
            
    d = mult_inv(e,r)
    public = (e,n)
    private = (d,n)
    return public,private

pus,prs=make_key(29,31)

# puc=(997,323)
# pus=(997,899)
# prs=(733,899)

def encrypt(pub_key,n_text):
    e,n=pub_key
    x=""
    m=0
    for i in n_text:
        if(i.isspace()):
            spc=400
            x+='*'
        else:               
            m= ord(i)
            c=(m**e)%n
            x+=chr(c)
    return x

def decrypt(priv_key,c_text):
    d,n=priv_key
    x=''
    m=0
    for i in c_text:
        if(i=='*'):
            x+=' '
        else:
            m=(ord(i)**d)%n
            c=chr(m)
            x+=c
    return x

def multithreaded_client(c, addr, name,puc):
    # sends the message to the client
    while True:
        # Establish connection with client.
        # ---------------------------------------------------------------------------------------------------------------------
        # Message recieved from the client and prints in the terminal
        msg = c.recv(1024).decode()

        print("-> Encrypted message:", msg)
        
        print(f'-> Received Message from {name.decode()}:', decrypt(prs,msg))
        str = input(f"Reply to {name.decode()}: ")
        str1=encrypt(puc,str)
        
        c.send(str1.encode())


while True:
    c, addr = s.accept()  # accept() returns a tuple

    name = c.recv(1024)

    p=""
    for ch in pus:   p+=str(ch)+','
    c.send(p.encode())
    
    p1=(c.recv(1024)).decode()
    pk=p1.split(',')
    puc=(int(pk[0]),int(pk[1]))

    print('Got connected with', addr, name.decode(),'Public Key: ',puc)


    # a = start_new_thread(multithreaded_client, (c, addr,))
    t1 = threading.Thread(target=multithreaded_client, args=(c, addr, name,puc))
    t1.start()
    
    print('Thread Count: ' + str(threading.active_count()))
    ThreadCount += 1
