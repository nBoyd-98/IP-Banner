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
	#LogParse.logread('/var/log/auth.log') 
	
	#Use this to test functionality independent of gui 

	myserver = Server("host", "user", "pass", "nick")
	f= myserver.get_firewall_fails()
	print(f)


def StartWindow():

	start_window = Tk()
	start_window.title("IP Banner")
	start_window.geometry("600x400")
	start_window.resizable(0, 0)

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
	login_window.resizable(0, 0)

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
				new_server.load_info()
				print("loading info.. whitelist: " + str(new_server.whitelist))
				admin.load_server(new_server)
			login_window.destroy()
			MainWindow(admin)

	confirm_btn = Button(login_window, text = "Confirm", command = confirm_clicked)
	confirm_btn.grid(row = 5, column = 1)

########################################################################################


def CreateWindow():
	login_window = Tk()
	login_window.title("New Admin Creation")
	login_window.geometry("600x400")
	login_window.resizable(0, 0)

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

######## START OF MAIN PROGRAM ###############################
def MainWindow(newadmin):
	mw = Tk()
	mw.geometry("600x400")
	mw.title("Main Window")
	lbl = Label(mw, text= "Logged in as: " + newadmin.username, font=(35))
	lbl.grid(row = 0, column = 0)

	def server_clicked():
		NewServerWindow(newadmin)

	def vs_clicked():
		ViewServersWindow(newadmin)
		mw.destroy()

	s_btn = Button(mw, text="New Server", command = server_clicked)
	s_btn.grid(row=2, column=0, pady = 10)
	s_btn.config(height=1, width=15)

	vs_btn = Button(mw, text="View Servers", command = vs_clicked)
	vs_btn.grid(row=3, column=0)
	vs_btn.config(height=1, width=15)

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

	def clicked(server, admin):
		ServerViewer(server, admin)
		vs.destroy()

	def backclicked(admin):
		MainWindow(admin)
		vs.destroy()

	vs = Tk()
	vs.resizable(0, 0)
	vs.geometry("600x400")
	vs.title("Server Viewer")
	i = 0
	for server in admin.serverdict.values():
		btn = Button(vs, text = server.alias, command = partial(clicked, server, admin), height=1, width=15)
		btn.grid(row=i, column=0)
		i+=1

	backbtn = Button(vs, text = "Back", command = partial(backclicked, admin)).grid(row = i+1, column=1, padx = 350, pady = 50)

def ServerViewer(server, admin):
	def wlclicked(server, admin):
		WhitelistEditWindow(server, admin)
		sv.destroy()
	def blclicked(server, admin):
		BlacklistEditWindow(server, admin)
		sv.destroy()
	def fwclicked(server, admin):
		FirewallEditWindow(server, admin)
		sv.destroy()
	def rmclicked(server, admin):
		RemoveWindow(server,admin)
		sv.destroy()
	def backclicked(admin):
		ViewServersWindow(admin)
		sv.destroy()
	sv = Tk()
	sv.title("Server Information")
	sv.geometry('600x400')
	sv.resizable(0, 0)
	hl = Label(sv, text = "Host: " + server.host).grid(row=0, column=0)
	hn = Label(sv, text = "Username: " + server.username).grid(row=1, column=0)
	ha = Label(sv, text = "Nickname: " + server.alias).grid(row=2, column=0)
	wlbtn = Button(sv, text = "Edit Whitelist", command = partial(wlclicked, server, admin), height = 1, width = 15)
	wlbtn.grid(row=3, column=0)
	blbtn = Button(sv, text = "Edit Blacklist", command = partial(blclicked, server, admin), height = 1, width = 15)
	blbtn.grid(row=3, column=1)
	fwbtn = Button(sv, text = "Edit Firewall", command = partial(fwclicked, server, admin), height = 1, width = 15)
	fwbtn.grid(row=3, column=2)
	rmbtn = Button(sv, text = "Remove Server", command = partial(rmclicked, server, admin), height = 1, width = 15)
	rmbtn.grid(row=3, column=4)
	backbtn = Button(sv, text = "Back", command = partial(backclicked, admin))
	backbtn.grid(row=4, column=4, padx=20, pady=20)

def FirewallEditWindow(server, admin):
	def failclicked(server, admin):
		print('hi')
	def timeclicked(server, admin):
		print('hi')
	fwe = Tk()
	fwe.geometry('600x400')
	fwe.title("Firewall Editor")
	fwe.resizable(0, 0)
	faillbl = Label(fwe, text = "Fails allowed / min: " + str(server.get_firewall_fails())).grid(row=0, column=0)
	failbtn = Button(fwe, text = "Edit", command = partial(failclicked, server, admin)).grid(row=0, column=1)
	timelbl = Label(fwe, text = "Ban time (min): " + str(server.get_firewall_time())).grid(row=1, column=0)
	timebtn = Button(fwe, text = "Edit", command = partial(timeclicked, server, admin)).grid(row=1, column=1)

def WhitelistEditWindow(server, admin):
	def addclicked(server, admin):
		AddWhitelistWindow(server, admin)
		wle.destroy()

	def rmclicked(server, ip):
		RemoveWhitelistWindow(server, ip)
		wle.destroy()

	def backclicked(server, admin):
		ServerViewer(server, admin)
		wle.destroy()

	wle = Tk()
	wle.geometry('600x400')
	wle.title("Whitelist Editor")
	wle.resizable(0, 0)

	addbtn = Button(wle, text="Add", command = partial(addclicked, server, admin)).grid(row=0, column=0)
	i = 1
	wl = server.get_whitelist()
	for ip in wl:
		iplabel = Label(wle, text = 'IP: ' + str(ip)).grid(row=i, column=0)
		rmbtn = Button(wle, text = "Remove", command = partial(rmclicked, server, ip)).grid(row=i, column=1)
		i += 1

	backbtn = Button(wle, text = "Back", command = partial(backclicked, server, admin))
	backbtn.grid(row = i+1, column=2, padx=15, pady=15)

def RemoveWhitelistWindow(server, ip):
	def yesclicked(server, ip):
		server.remove_whitelist(ip)
		rmwl.destroy()

	def noclicked():
		rmwl.destroy()
	rmwl = Tk()
	rmwl.geometry('600x400')
	lbl = Label(rmwl, text = "Are you sure you want to remove " + str(ip) + "?").grid(row=0, column=0)
	yesbtn = Button(rmwl, text = "Yes", command = partial(yesclicked, server, ip)).grid(row=1, column=0)
	nobtn = Button(rmwl, text = "No", command = noclicked)

def AddWhitelistWindow(server, admin):
	def addclicked(server, admin):
		ip = ipentry.get()
		try:
			server.add_whitelist(ip)
			addwl.destroy()
			WhitelistEditWindow(server, admin)
		except:
			lbl = Label(addwl, text = "IP already in whitelist").grid(row=2, column=0)
	addwl = Tk()
	addwl.geometry('600x400')
	addlbl = Label(addwl, text="IP address to add to whitelist: ").grid(row=0, column=0)
	ipentry = Entry(addwl)
	ipentry.grid(row=0, column=1)
	addbtn = Button(addwl, text = "Add", command = partial(addclicked, server, admin)).grid(row=1, column=0)


##########################################################################################


def BlacklistEditWindow(server, admin):
	def addclicked(server, admin):
		AddBlacklistWindow(server, admin)
		ble.destroy()

	def rmclicked(server, ip):
		RemoveBlacklistWindow(server, ip)
		ble.destroy()

	def backclicked(server, admin):
		ServerViewer(server, admin)
		ble.destroy()

	ble = Tk()
	ble.geometry('600x400')
	ble.title("Blacklist Editor")
	ble.resizable(0, 0)

	addbtn = Button(ble, text="Add", command = partial(addclicked, server, admin)).grid(row=0, column=0)
	i = 1
	bl = server.get_blacklist()
	for ip in bl:
		iplabel = Label(ble, text = 'IP: ' + str(ip)).grid(row=i, column=0)
		rmbtn = Button(ble, text = "Remove", command = partial(rmclicked, server, ip)).grid(row=i, column=1)
		i += 1

	backbtn = Button(ble, text = "Back", command = partial(backclicked, server, admin))
	backbtn.grid(row = i+1, column=2, padx=15, pady=15)

def RemoveBlacklistWindow(server, ip):
	def yesclicked(server, ip):
		server.remove_blacklist(ip)
		rmbl.destroy()

	def noclicked():
		rmbl.destroy()

	rmbl = Tk()
	rmbl.geometry('600x400')
	lbl = Label(rmbl, text = "Are you sure you want to remove " + str(ip) + "?").grid(row=0, column=0)
	yesbtn = Button(rmbl, text = "Yes", command = partial(yesclicked, server, ip)).grid(row=1, column=0)
	nobtn = Button(rmbl, text = "No", command = noclicked)

def AddBlacklistWindow(server, admin):
	def addclicked(server, admin):
		ip = ipentry.get()
		try:
			server.add_blacklist(ip)
			addbl.destroy()
			BlacklistEditWindow(server, admin)
		except:
			lbl = Label(addbl, text = "IP already in blacklist").grid(row=2, column=0)
	addbl = Tk()
	addbl.geometry('600x400')
	addlbl = Label(addbl, text="IP address to add to blacklist: ").grid(row=0, column=0)
	ipentry = Entry(addbl)
	ipentry.grid(row=0, column=1)
	addbtn = Button(addbl, text = "Add", command = partial(addclicked, server, admin)).grid(row=1, column=0)





##Remove Server
def RemoveWindow(server, admin):
	def yesclicked(server, admin):
		admin.remove_server(server)
		rw.destroy()

	def noclicked():
		rw.destroy()

	rw = Tk()
	rw.geometry('600x400')
	rw.title("Remove Server")
	rw.resizable(0, 0)
	rl = Label(rw, text = "Are you sure you want to remove this server?").grid(row=0, column=0)
	yesbtn = Button(rw, text = "Yes", command = lambda: yesclicked(server, admin))
	yesbtn.grid(row=1, column=0)
	nobtn = Button(rw, text = "No", command = noclicked())
	nobtn.grid(row=1, column=1)








StartWindow()
#main()
