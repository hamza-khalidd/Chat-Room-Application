import socket
import sys

s = socket.socket()
s.connect(("localhost",5050))
if len(sys.argv) != 2:
    print("Correct usage: script, Filename with extension")
    exit()
a=sys.argv[1]
f = open(a, "rb")
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)
s.close()