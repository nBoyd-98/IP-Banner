#!/usr/bin/python3

from Admin import Admin
from Server import Server
from DatabaseHelper import DatabaseHelper
import LogParse
import FirewallBan
import time
import subprocess
from functools import partial
from tkinter import *



def main():
	print("Hello")
	# logread() runs a while True: loop and expects to be the last thing running
	# Currently authlog path is hard coded but this will change to be a config
	# Variable as more OS's become supported
	LogParse.logread('/var/log/auth.log') 
	
	#Use this to test functionality independent of gui 


def StartWindow():

	start_window = Tk()
	start_window.title("IP Banner")
	start_window.geometry("600x400")

	def login_clicked():
		start_window.destroy()
		LoginWindow()

	login_btn = Button(start_window, text="Login", command = login_clicked)
	login_btn.grid(column = 1, row = 0)

	def new_clicked():
		start_window.destroy()
		CreateWindow()

	new_btn = Button(start_window, text="New Admin", command = new_clicked)
	new_btn.grid(column = 2, row = 0)
	start_window.mainloop()

def LoginWindow():
	login_window = Tk()
	login_window.title("Account Login")
	login_window.geometry("600x400")

	lbl = Label(login_window, text = "Please provide username and password")
	lbl.grid(row = 0, column = 0)

	usr_lbl = Label(login_window, text = "Username: ")
	usr_lbl.grid(row = 2, column = 0)
	e1 = Entry(login_window)
	e1.grid(row = 2, column = 1)

	psw_label = Label(login_window, text = "Password: ")
	psw_label.grid(row = 3, column = 0)
	e2 = Entry(login_window, show = "*")
	e2.grid(row = 3, column = 1)

	def confirm_clicked():
		name = e1.get()
		psw = e2.get()
		myhelper = DatabaseHelper()
		good = myhelper.check_password(name, psw)
		if not good:
			fl = Label(login_window, text = "Sorry, incorrect username or password").grid(row=6, column=0)
		else:
			admin = Admin(name, psw)
			myhelper = DatabaseHelper()
			slist = myhelper.get_users_servers(admin.username)
			for server in slist:
				new_server = Server(server[0], server[1], server[2], server[3])
				admin.add_server(new_server)
			login_window.destroy()
			MainWindow(admin)

	confirm_btn = Button(login_window, text = "Confirm", command = confirm_clicked)
	confirm_btn.grid(row = 5, column = 1)

########################################################################################


def CreateWindow():
	login_window = Tk()
	login_window.title("New Admin Creation")
	login_window.geometry("600x400")

	lbl = Label(login_window, text = "Please create new username and password")
	lbl.grid(row = 0, column = 0)

	lbl2 = Label(login_window, text = "NOTE: This is a login for the system, not a server")
	lbl2.grid(row = 1, column = 0)

	usr_lbl = Label(login_window, text = "Username: ")
	usr_lbl.grid(row = 2, column = 0)
	e1 = Entry(login_window)
	e1.grid(row = 2, column = 1)

	psw_label = Label(login_window, text = "Password: ")
	psw_label.grid(row = 3, column = 0)
	e2 = Entry(login_window, show = "*")
	e2.grid(row = 3, column = 1)

	def confirm_clicked():
		name = e1.get()
		psw = e2.get()
		myhelper = DatabaseHelper()
		hasname = myhelper.check_user(name)
		if hasname:
			fail_lbl = Label(login_window, text = "Sorry, username already exists")
			fail_lbl.grid(row = 6, column = 1)
		elif (20>len(name)<3):
			fail_lbl = Label(login_window, text = "Invalid username length")
			fail_lbl.grid(row = 6, column = 1)
		elif (32>len(psw)<6):
			fail_lbl = Label(login_window, text = "Invalid password length")
			fail_lbl.grid(row = 6, column = 1)

		else:
			newadmin = Admin(name, psw)
			myhelper.add_user(newadmin)
			login_window.destroy()
			MainWindow(newadmin)

	confirm_btn = Button(login_window, text = "Confirm", command = confirm_clicked)
	confirm_btn.grid(row = 5, column = 1)


def MainWindow(newadmin):
	mw = Tk()
	mw.geometry("600x400")
	lbl = Label(mw, text= "Logged in as: " + newadmin.username)
	lbl.grid(row = 0, column = 0)

	def server_clicked():
		NewServerWindow(newadmin)

	def vs_clicked():
		ViewServersWindow(newadmin)

	s_btn = Button(mw, text="New Server", command = server_clicked)
	s_btn.grid(row=2, column=0)

	vs_btn = Button(mw, text="View Servers", command = vs_clicked)
	vs_btn.grid(row=3, column=0)

def NewServerWindow(newadmin):
	sw = Tk()
	sw.geometry("600x400")
	lbl = Label(sw, text= "Provide credentials for new server", justify=LEFT, anchor="w")
	lbl.grid(row=0, column=0, sticky = W)
	host_lbl = Label(sw, text= "Host: ", justify=LEFT, anchor="w")
	host_lbl.grid(row=1, column=0, sticky = W) 
	usr_lbl = Label(sw, text= "Username: ", justify=LEFT, anchor="w")
	usr_lbl.grid(row=2, column=0, sticky= W)
	psw_lbl = Label(sw, text= "Password: ", justify=LEFT, anchor="w")
	psw_lbl.grid(row=3, column=0, sticky = W)
	nn_lbl = Label(sw, text= "Nickname: ", justify=LEFT, anchor="w")
	nn_lbl.grid(row=4, column=0, sticky = W)
	note_lbl = Label(sw, text = "NOTE: 'nickname' field is only for your convenience and is not a credetial to any server")
	note_lbl.grid(row=5, column=0, columnspan=3)

	h = Entry(sw)
	h.grid(row=1, column=0)
	u = Entry(sw)
	u.grid(row=2, column=0)
	p = Entry(sw, show = "*")
	p.grid(row=3, column=0)
	n = Entry(sw)
	n.grid(row=4, column=0)

	def confirm_clicked():
		host = h.get()
		user = u.get()
		password = p.get()
		alias = n.get()
		if int(len(host))<1 or int(len(user))<1 or int(len(password))<1 or int(len(alias))<1:
			f = Label(sw, text= "Sorry, no empty field allowed").grid(row=8, column=0)
		else:
			newserver = Server(host, user, password, alias)
			connect = newserver.test_login()
		if not connect:
			WarningWindow(newadmin, newserver, sw)
		else:
			newadmin.add_server(newserver)
			myhelper = DatabaseHelper()
			myhelper.add_server(newadmin.username, newserver)
			sw.destroy()

	btn = Button(sw, text="Confirm", command = confirm_clicked).grid(row=6, column=0)

def WarningWindow(newadmin, newserver, sw):
	ww = Tk()
	ww.geometry("600x400")
	lbl = Label(ww, text="Cannot establish valid connection with supplied credentials, continue anyway?")
	lbl.grid(row=0, column = 0)

	def yes():
		newadmin.add_server(newserver)
		myhelper = DatabaseHelper()
		myhelper.add_server(newadmin.username, newserver)
		ww.destroy()
		sw.destroy()
		MainWindow(newadmin)

	def no():
		ww.destroy()

	yb = Button(ww, text="Yes", command = yes)
	yb.grid(row=1, column=0)

	nb = Button(ww, text="No", command = no)
	nb.grid(row=1, column=1)


def ViewServersWindow(admin):
	def clicked(server):
		ServerViewer(server)

	vs = Tk()
	vs.geometry("600x400")
	i = 0
	for server in admin.serverdict.values():
		btn = Button(vs, text = server.alias, command = partial(clicked, server))
		btn.grid(row=i, column=0)
		i+=1

def ServerViewer(server):
	sv = Tk()
	sv.geometry('600x400')
	hl = Label(sv, text = "Host: " + server.host).grid(row=0, column=0)
	hn = Label(sv, text = "Username: " + server.username).grid(row=1, column=0)
	ha = Label(sv, text = "Nickname: " + server.alias).grid(row=2, column=0)







StartWindow()
#main()
