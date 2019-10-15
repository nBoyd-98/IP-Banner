#!/usr/bin/python3
from pexpect import pxssh

class Server():

	def __init__(self, host, username, password, alias):
		self.host = host
		self.username = username
		self.password = password
		self.alias = alias
		self.s = pxssh.pxssh()

	def server_login(self):
		if not (self.s.login(self.host, self.username, self.password)):
			print("fail on login")
			print(str(s))
		else:
			print("worked")

	def talk(self, command):
		self.s.sendline(command)
		self.s.prompt()
		print(self.s.before)




