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

	def list_users(self):
		self.db = sqlite3.connect('users.db')
		cursor = self.db.execute("SELECT ID, USERNAME, PASSWORD FROM USERS")
		for row in cursor:
			print("ID= " + str(row[0]))
			print("USERNAME= " + str(row[1]))
			print("PASSWORD= " + str(row[2]))
			print()

		self.db.close()
