#!/usr/bin/python3
from Server import Server
from DatabaseHelper import *

class Admin:
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.servercount = 0
		self.serverdict = {}
		self.serverlist = []

	def add_server(self, new_server):
		myhelper = DatabaseHelper()
		myhelper.add_server(self.username, new_server)
		self.serverdict[new_server.alias] = new_server
		self.serverlist.append(new_server)
		self.servercount += 1

	def load_server(self, server):
		self.serverdict[server.alias] = server
		self.serverlist.append(server)
		self.servercount += 1

	def remove_server(self, toremove):
		myhelper = DatabaseHelper()
		myhelper.remove_server(toremove)
		del self.serverdict[toremove.alias]
		self.servercount -= 1

	def get_server(self, alias):
		return self.serverdict[alias]

	def get_server_count(self):
		return self.servercount

