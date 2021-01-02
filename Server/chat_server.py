from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import smtplib as s
import socket
import threading
from subprocess import call
import ray

def mainGUI():
	window = Tk()
	window.resizable(0, 0)
	window.title('Host Server')
	window.geometry('500x400+550+200')
	photo = PhotoImage(file="mainimage.png")
	label = Label(window, image=photo)
	label.pack()
	btnmeeting = Button(window, text="Send ChatRoom Details", bg='white', relief='flat', width=20,
						font=('Montserrat', 15, 'bold'), command=sendemails).place(x=100, y=210)
	btnstudent = Button(window, text="Add Users", bg='white', relief='flat', width=20,
						font=('Montserrat', 15, 'bold'), command=addstudents).place(x=100, y=270)
	btnopenmeet = Button(window, text="Create ChatRoom", bg='white', relief='flat', width=20,
						 font=('Montserrat', 15, 'bold'), command=mainfunctionforSERVER).place(x=100, y=330)
	window.mainloop()

def sendemails():
    ob = s.SMTP("smtp.gmail.com", 587)
    ob.starttls()
    ob.login("hosthamzabychitchat@gmail.com", "hosthamzabychitchat@1")
    subject = "Meeting Credentials"
    body = "Join The Group Meeting By Opening ChitChat App and enter the port number: 12345 \n IP: localhost"
    message = "Subject:{}\n\n{}".format(subject, body)
    file = open("emailids.txt", "r")
    for i in file:
        ob.sendmail("hosthamzabychitchat@gmail.com", i, message)
    messagebox.showinfo("Command Completed", "Email Is Send To Students")
    ob.quit()

def addstudents():
    # Enter Port Number Create Meeting Room & Send Email To Students
    window = Toplevel()
    window.resizable(0, 0)
    window.title('Create Meeting')
    window.geometry('500x400+550+200')
    photo = PhotoImage(file="addstudents.png")
    label = Label(window, image=photo)
    label.pack()

    global em
    em = StringVar()
    global em_txt
    em_txt = Entry(window, textvar=em, bg='white', font=('Montserrat', 15, 'bold')).place(x=105, y=210)
    button = Button(window, text='Create Group Chat', bg='white', width=25, command=None)
    btnadd = Button(window, text="Add Student", bg='white', relief='flat', width=20,
                          font=('Montserrat', 15, 'bold'), command=savestudenttofile).place(x=100, y=270)
    window.mainloop()

def savestudenttofile():
    email = em.get()
    f = open("emailids.txt", "a+")
    f.write('\n'+email)
    f.close()
    messagebox.showinfo("Command Completed", "Student Added Successfully")

def mainfunctionforSERVER():
	ray.init()
	@ray.remote
	def func1():
		exec(open('upload_server.py').read())

	@ray.remote
	def func2():
		#exec(open('dwnld_server.py').read())
		call(["python", "dwnld_server.py"])

	@ray.remote
	def func3():
		PORT = 12345
		SERVER = 'localhost'

		ADDRESS = (SERVER, PORT)

		FORMAT = "utf-8"

		clients, names = [], []

		server = socket.socket(socket.AF_INET,
							   socket.SOCK_STREAM)

		server.bind(ADDRESS)

		def startChat():

			print("server is working on " + SERVER)
			server.listen()

			while True:
				conn, addr = server.accept()
				conn.send("NAME".encode(FORMAT))
				name = conn.recv(1024).decode(FORMAT)

				names.append(name)
				clients.append(conn)

				print(f"Name is :{name}")

				broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

				conn.send('Connection successful!'.encode(FORMAT))

				thread = threading.Thread(target=handle,
										  args=(conn, addr))
				thread.start()

				print(f"active connections {threading.activeCount() - 1}")

		def handle(conn, addr):

			print(f"new connection {addr}")
			connected = True

			while connected:
				message = conn.recv(1024)
				broadcastMessage(message)

			conn.close()

		def broadcastMessage(message):
			for client in clients:
				client.send(message)

		startChat()

	ray.get([func1.remote(), func2.remote(), func3.remote()])
#-------------------------
mainGUI()