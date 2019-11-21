#!/usr/bin/python3

class Firewall():

	def __init__(self):
		self.fails = 10
		self.ban_minutes = 100

	def get_fails(self):
		return self.fails

	def get_bantime(self):
		return self.ban_minutes

	def change_firewall(self, Server, fails, bantime):
		myhelper = DatabaseHelper()
		myhelper.change_firewall_fails(Server, fails)
		self.fails = fails
		
		myhelper.change_firewall_time(Server, bantime)
		self.ban_minutes = bantime

		return True

	def change_firewall_fails(self, Server, fails):
		myhelper = DatabaseHelper()
		myhelper.change_firewall_fails(Server, fails)
		self.fails =  fails
		return True

	def change_firewall_time(self, Server, bantime):
		myhelper = DatabaseHelper()
		myhelper.change_firewall_time(Server, bantime)
		self.ban_minutes = bantime
		return True
