import socket
import sys
s = socket.socket()
s.bind(("localhost",5050))
s.listen(10)

i=1

while True:
    print("Upload server is Waiting... ")
    sc, address = s.accept()
    print(address)

    f = open('file.txt','wb') #open in binary
    i=i+1
    print(i)
    l = 1
    while(l):
        l = sc.recv(1024)
        while (l):
            f.write(l)
            l = sc.recv(1024)
        f.close()


    sc.close()
s.close()