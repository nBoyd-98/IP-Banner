#!/usr/bin/python3
from pexpect import pxssh

class Server():

	def __init__(self, host, username, password, alias):
		self.host = host
		self.username = username
		self.password = password
		self.alias = alias
		self.s = pxssh.pxssh()

	def test_login(self):
		try:
			(self.s.login(self.host, self.username, self.password))
			self.s.logout()
			return True
		except:
			return False

	def send_line(self, command):
		self.s.sendline(command)
		line = self.s.prompt()
		return line




