#!/usr/bin/python3
from pexpect import pxssh
from Firewall import *
from DatabaseHelper import *

class Server():

	def __init__(self, host, username, password, alias):
		self.host = host
		self.username = username
		self.password = password
		self.alias = alias
		self.s = pxssh.pxssh()
		self.whitelist = []
		self.blacklist = []
		self.firewall = Firewall()

	def test_login(self):
		try:
			(self.s.login(self.host, self.username, self.password))
			self.s.logout()
			return True
		except:
			return False

	def get_firewall_fails(self):
		return self.firewall.fails

	def get_firewall_time(self):
		return self.firewall.ban_minutes

	def load_info(self):
		myhelper = DatabaseHelper()
		wl = myhelper.get_whitelist(self)
		for tup in wl:
			for ip in tup:
				self.whitelist.append(ip)
		bl = myhelper.get_blacklist(self)
		for tup in bl:
			for ip in tup:
				self.blacklist.append(ip)
		fw = myhelper.get_firewall(self)
		for tup in fw:
			try:
				self.firewall = Firewall(tup[0], tup[1])
			except:
				print("default firewall")


	def get_firewall(self):
		return self.firewall


	def get_whitelist(self):
		print("in server " + str(self.whitelist))
		return self.whitelist

	def add_whitelist(self, tolist):
		myhelper = DatabaseHelper()
		valid = myhelper.add_whitelist(self, tolist)
		if valid:
			self.whitelist.append(tolist)
			return True
		else:
			print("nope")
			return False

	def remove_whitelist(self, toremove):
		self.whitelist.remove(toremove)
		myhelper =  DatabaseHelper()
		myhelper.remove_whitelist(self, toremove)


	def add_blacklist(self, tolist):
		myhelper = DatabaseHelper()
		valid = myhelper.add_blacklist(self, tolist)
		if valid:
			self.blacklist.append(tolist)
			return True
		else:
			return False

	def remove_blacklist(self, toremove):
		self.blacklist.remove(toremove)
		myhelper =  DatabaseHelper()
		myhelper.remove_blacklist(self, toremove)

	def get_blacklist(self):
		return self.blacklist


	def send_line(self, command):
		self.s.sendline(command)
		line = self.s.prompt()
		return line




