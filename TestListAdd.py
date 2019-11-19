#!/usr/bin/python3

import unittest
from DatabaseHelper import *
from Server import *

class TestWhitelistAdd(unittest.TestCase):


	def test_add_valid(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		self.assertTrue(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, "168.0.1.1"))

	def test_add_text(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		self.assertFalse(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, "garbage"))

	def test_add_invalid(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		self.assertFalse(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, "9999.9999.9999"))

	def test_add_empty(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		self.assertFalse(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, ""))

	def test_add_off_by_one(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		self.assertFalse(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, "168.199.2311.2"))

	def test_add_in_blacklist(self):
		testserver = Server("ahost", "ausername", "apass", "anickname")
		ip = "123.5.4.3"
		DatabaseHelper.add_blacklist(DatabaseHelper, testserver, ip)
		self.assertFalse(DatabaseHelper.add_whitelist(DatabaseHelper, testserver, ip))


if __name__ == "__main__":
	unittest.main()
