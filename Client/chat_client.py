import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sys
import subprocess

class GUI:
    def __init__(self, client, FORMAT):
        self.filestatus=False
        self.client = client
        self.FORMAT = FORMAT

        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.photo = PhotoImage(file="connectmeeting.png")
        self.label = Label(self.login, image=self.photo)
        self.label.pack()

        #self.pls = Label(self.login, text="Please Enter Your Name", justify=CENTER, font="Helvetica 14 bold").place(relheight=0.15, relx=0.2, rely=0.07)
        self.labelName = Label(self.login, text="Name: ", font="Helvetica 14", bg='#878a8c', fg='White').place(relheight=0.1, relx=0.2, rely=0.4)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4)
        self.entryName.focus()

        self.go = Button(self.login, text="CONTINUE", font="Helvetica 14 bold", bg='#878a8c', fg='White', command=lambda: self.goAhead(self.entryName.get())).place(relx=0.4, rely=0.6)

        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self , name):
        self.name = name

        self.Window.deiconify()
        self.Window.title("CHAT-ROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=800, height=600, bg="#17202A")

        self.labelHead = Label(self.Window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold",
                               pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14",
                             padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.64, relheight=0.03, rely=0.020, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=10, bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.68, rely=0.020, relheight=0.03, relwidth=0.08)

        self.buttonMsg1 = Button(self.labelBottom, text="SendFile", font="Helvetica 10 bold", width=20,
                                 bg="#ABB2B9",
                                 command=self.my_file)
        self.buttonMsg1.place(relx=0.775, rely=0.020, relheight=0.03, relwidth=0.11)

        self.buttonMsg2 = Button(self.labelBottom, text="GetFile", font="Helvetica 10 bold", width=20,
                                 bg="#ABB2B9", command=self.getfile)
        self.buttonMsg2.place(relx=0.90, rely=0.020, relheight=0.03, relwidth=0.08)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def my_file(self):
        filename = filedialog.askopenfilename(initialdir="C:/", title="select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        self.Runfile(filename)

    def Runfile(self, msg):
        if msg == "":
            messagebox.showinfo("Error", "Enter file name in the field")
        else:
            subprocess.call([sys.executable , 'upload_client.py', msg])
            self.filestatus=True
            self.sendButton('File Uploaded')

    def getfile(self):
        #filename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        subprocess.call([sys.executable, 'dwnld_client.py', 'file.txt'])

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(self.FORMAT)
                if message == 'NAME':
                    self.client.send(self.name.encode(self.FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

            except:
                print("An error occured!")
                self.client.close()
                break

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            self.client.send(message.encode(self.FORMAT))
            break


def input():
    window = Tk()
    window.resizable(0, 0)
    window.title('Join Client')
    window.geometry('500x400+550+200')
    photo = PhotoImage(file="mainimage.png")
    label = Label(window, image=photo)
    label.pack()
    labelName = Label(window, text="Port: ", bg='#838689', font="Helvetica 12 bold", fg='white').place(relheight=0.1, relx=0.2, rely=0.32)
    labelName2 = Label(window, text="  Ip :  ", bg='#838689', font="Helvetica 12 bold", fg='white').place(relheight=0.1, relx=0.2, rely=0.52)
    global prt
    prt = StringVar()
    global ipp
    ipp = StringVar()
    entryName = Entry(window, font="Helvetica 14", textvar=prt).place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.3)
    entryName = Entry(window, font="Helvetica 14", textvar=ipp).place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.5)
    btnadd = Button(window, text="Verify", bg='darkgray', relief='flat', width=20, fg='white', font=('Montserrat', 15, 'bold'), command=lambda: connect(window)).place(x=120, y=300)

    window.mainloop()


def connect(form):
    PORT = int(prt.get())
    SERVER = ipp.get()
    ADDRESS = (SERVER, PORT)
    FORMAT = "utf-8"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    form.destroy()
    g = GUI(client, FORMAT)

input()