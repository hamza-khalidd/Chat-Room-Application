import socket
import threading
import os

class Server :
    def __init__(self) :
        self.accept_connections()

    def accept_connections(self) :
        ip = 'localhost'
        port = 1024

        self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.s.bind((ip , port))
        self.s.listen(100)

        print('Download Server Running')

        while 1 :
            c , addr = self.s.accept()
            print(c)

            threading.Thread(target=self.handle_client , args=(c , addr ,)).start()

    def handle_client(self , c , addr) :
        data = c.recv(1024).decode()

        if not os.path.exists(data) :
            c.send("file-doesn't-exist".encode())

        else :
            c.send("file-exists".encode())
            print('Sending' , data)
            if data != '' :
                file = open(data , 'rb')
                data = file.read(1024)
                while data :
                    c.send(data)
                    data = file.read(1024)

                c.shutdown(socket.SHUT_RDWR)
                c.close()


s = Server()