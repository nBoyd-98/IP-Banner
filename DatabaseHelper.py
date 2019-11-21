#!/usr/bin/python3
import sqlite3
import re

from FirewallBan import *

class DatabaseHelper():

	def __init__(self):
		self.db = sqlite3.connect('users.db')
		self.db.execute('''CREATE TABLE IF NOT EXISTS USERS
			(ID INTEGER PRIMARY KEY   AUTOINCREMENT, 
			 USERNAME      TEXT   NOT NULL, 
			 PASSWORD      TEXT   NOT NULL);''')
	
		self.db.execute('''CREATE TABLE IF NOT EXISTS SERVERS
			(ID         INTEGER   NOT NULL,
			HOST          TEXT    NOT NULL,
			USER          TEXT    NOT NULL, 
			PASSWORD      TEXT    NOT NULL, 
			ALIAS         TEXT    NOT NULL);''')

		self.db.execute('''CREATE TABLE IF NOT EXISTS WHITELIST
			(ALIAS TEXT NOT NULL,
			IP     TEXT NOT NULL UNIQUE);''')

		self.db.execute('''CREATE TABLE IF NOT EXISTS BLACKLIST
			(ALIAS TEXT NOT NULL,
			IP     TEXT NOT NULL UNIQUE);''')

	def add_user(self, Admin):
		username = Admin.username
		password = Admin.password
		self.db = sqlite3.connect('users.db')
		self.db.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES(?, ?);", (username, password))
		self.db.commit()
		self.db.close()

	def check_user(self, username):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.cursor()
		cursor.execute('''SELECT USERNAME FROM USERS WHERE USERNAME=?''', (username,))
		user = cursor.fetchone()
		self.db.close()
		if user:
			return True
		else:
			return False

	def get_id(self, username):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.cursor()
		cursor.execute('''SELECT ID FROM USERS WHERE USERNAME = ?''', (username,))
		num = cursor.fetchone()
		return num[0]

	def check_password(self, username, password):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.cursor()
		cursor.execute('''SELECT PASSWORD FROM USERS WHERE USERNAME = ?''', (username,))
		psw = cursor.fetchone()
		self.db.close()
		if not psw:
			return False
		elif (password == psw[0]):
			return True
		else:
			return False

	def change_password(self, username, oldpass, newpass):
		testold = self.check_password(username, oldpass)
		if not testold:
			return False
		self.db = sqlite3.connect('users.db')
		self.db.execute('''UPDATE USERS SET PASSWORD = ? WHERE USERNAME = ? ''', (newpass, username))
		self.db.commit()
		self.db.close()
		return True

	def list_users(self):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.execute("SELECT ID, USERNAME, PASSWORD FROM USERS")
		for row in cursor:
			print("ID= " + str(row[0]))
			print("USERNAME= " + str(row[1]))
			print("PASSWORD= " + str(row[2]))
			print("test")
		self.db.close()

	def add_server(self, owner, Server):
		self.db = sqlite3.connect('users.db')
		num = self.get_id(owner)
		self.db.execute("INSERT INTO SERVERS (ID, HOST, USER, PASSWORD, ALIAS) VALUES(?, ?, ?, ?, ?);" ,(num, Server.host, Server.username, Server.password, Server.alias))
		self.db.commit()
		self.db.close()

	def remove_server(self, Server):
		self.db = sqlite3.connect('users.db')
		name = Server.alias
		try:
			self.db.execute("DELETE FROM SERVERS WHERE ALIAS = ?",(name,))
			self.db.commit()
			self.db.close()
		except:
			return False
		return True


	def get_users_servers(self, owner):
		self.db = sqlite3.connect('users.db')
		num = self.get_id(owner)
		cursor = self.db.cursor()
		cursor.execute('''SELECT HOST, USER, PASSWORD, ALIAS FROM SERVERS WHERE ID = ? ''' ,(num,))
		servers = cursor.fetchall()
		return servers

	def get_server(self, alias):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.cursor()
		cursor.execute('''SELECT HOST, USER, PASSWORD, ALIAS FROM SERVERS WHERE ALIAS = ? ''' , (alias,))
		server = cursor.fetchone()
		return server

	def add_blacklist(self, Server, tolist):
		ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		test = ip_pat.match(tolist)
		if not test:
			return False
		else:
			wlist = self.get_whitelist(Server)
			for white_ip in wlist:
				for ip in white_ip:
					if ip == tolist:
						return False
		self.db = sqlite3.connect('users.db')
		self.db.execute("INSERT INTO BLACKLIST (ALIAS, IP) VALUES(?, ?);" ,(Server.alias, tolist))
		self.db.commit()
		self.db.close()
		ban_ip(tolist)
		return True

	def remove_blacklist(self, Server, toremove):
		self.db = sqlite3.connect('users.db')
		try:
			self.db.execute("DELETE FROM BLACKLIST WHERE IP = ?", (toremove,))
			self.db.commit()
			self.db.close()
		except:
			return False
		return True

	def get_blacklist(self, Server):
		self.db = sqlite3.connect('users.db')
		alias = Server.alias
		cursor = self.db.cursor()
		cursor.execute('''SELECT IP FROM BLACKLIST WHERE ALIAS = ? ''' ,(alias,))
		blacklist = cursor.fetchall()
		return blacklist

	def add_whitelist(self, Server, tolist):
		ip_pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		test = ip_pat.match(tolist)
		if not test:
			return False
		else:
			blist = self.get_blacklist(Server)
			for black_ip in blist:
				for ip in black_ip:
					if ip == tolist:
						return False
		self.db = sqlite3.connect('users.db')
		self.db.execute("INSERT INTO WHITELIST (ALIAS, IP) VALUES(?, ?);" ,(Server.alias, tolist))
		self.db.commit()
		self.db.close()
		return True

	def remove_whitelist(self, Server, toremove):
		self.db = sqlite3.connect('users.db')
		try:
			self.db.execute("DELETE FROM WHITELIST WHERE IP = ?", (toremove,))
			self.db.commit()
			self.db.close()
		except:
			return False
		return True

	def get_whitelist(self, Server):
		self.db = sqlite3.connect('users.db')
		alias = Server.alias
		cursor = self.db.cursor()
		cursor.execute('''SELECT IP FROM WHITELIST WHERE ALIAS = ? ''' ,(alias,))
		whitelist = cursor.fetchall()
		print("in database " + str(whitelist))
		return whitelist



