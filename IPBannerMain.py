#!/usr/bin/python3
from Admin import Admin
from Server import Server
from DatabaseHelper import DatabaseHelper
from tkinter import *

def main():
	myhelper = DatabaseHelper()
	myhelper.add_entry("user1", "pass2")
	myhelper.add_entry("user2", "pass2")
	myhelper.list_users()

def StartWindow():
	start_window = Tk()
	start_window.title("IP Banner")
	start_window.geometry("600x400")

	def login_clicked():
		login_btn.configure(text = "clicked")
	login_btn = Button(start_window, text="Login", command = login_clicked)
	login_btn.grid(column = 1, row = 0)

	def new_clicked():
		start_window.destroy()
		CreateWindow()
	new_btn = Button(start_window, text="New Admin", command = new_clicked)
	new_btn.grid(column = 2, row = 0)
	start_window.mainloop()

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
		#We now need to save this info to a database


	confirm_btn = Button(login_window, text = "Confirm", command = confirm_clicked)



#StartWindow()

#main()