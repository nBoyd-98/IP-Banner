#!/usr/bin/python3
import sqlite3

class DatabaseHelper():

	def __init__(self):
		self.db = sqlite3.connect('users.db')
		self.db.execute('''CREATE TABLE IF NOT EXISTS USERS
			(ID INTEGER PRIMARY KEY   AUTOINCREMENT, 
			 USERNAME      TEXT   NOT NULL, 
			 PASSWORD      TEXT   NOT NULL);''')
		self.db.close()

	def add_entry(self, username, password):
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

	def check_password(self, username, password):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.cursor()
		cursor.execute('''SELECT PASSWORD FROM USERS WHERE USERNAME=?''', (username,))
		psw = cursor.fetchone()
		self.db.close()
		if (password == psw[0]):
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
			print()

		self.db.close()
