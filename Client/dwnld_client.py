import socket
import os
import sys

if len(sys.argv) != 2:
    print("Correct usage: script, Filename with extension")
    exit()

a=sys.argv[1]
class Client :
    def __init__(self) :
        self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self) :
        self.target_ip = 'localhost'
        self.target_port = 1024

        self.s.connect((self.target_ip , int(self.target_port)))

        self.main()

    def reconnect(self) :
        self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.s.connect((self.target_ip , int(self.target_port)))

    def main(self):
        while 1:
            file_name = a
            self.s.send(file_name.encode())

            confirmation = self.s.recv(1024)
            if confirmation.decode() == "file-doesn't-exist" :
                print("File doesn't exist on server.")

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

            else :
                write_name = 'from_server ' + file_name
                if os.path.exists(write_name) : os.remove(write_name)

                with open(write_name , 'wb') as file :
                    while 1 :
                        data = self.s.recv(1024)

                        if not data :
                            break

                        file.write(data)

                print(file_name , 'successfully downloaded.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()
                break


client = Client()