import socket
import math
import random
import pickle
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 1234

# connect to the server on local computer
s.connect(('192.168.43.64', port))

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

puc,prc=make_key(17,19)


# puc=(997,323)
# prc=(13,323)
# pus=(997,899)



# -----------------------------------------------------------------------------------------------------------------------


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

name = input("Enter your name: ")
s.send(name.encode())

p1=(s.recv(1024)).decode()
pk=p1.split(',')
pus=(int(pk[0]),int(pk[1]))
print('Got connected with server, Public Key',pus)

p=""
for c in puc:
    p+=str(c)+','
s.send(p.encode())




while True:
    # Take input from the client and send it to the server
    data = input("------> ")

    mes = encrypt(pus,data)

    s.send(mes.encode())

    # Receive the message from the server and print it in the terminal
    msg = s.recv(1024).decode()
    
    print("-> Encrypted message:", msg)
    
    print("-> Recieved message from the server:", decrypt(prc,msg))
    # s.close()
