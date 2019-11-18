#!/usr/bin/env python3 

import unittest

from Server import *

class TestServerAdd(unittest.TestCase):

	def test_add(self):
		self.assertTrue(Server("testHost", "testUser", "testPass", "testNick")) #test can add server

	def test_missing_argument(self):
		self.assertRaises(TypeError, Server, "host", "user", "pswd") #test if raise exception when missing argument
		
if __name__ == "__main__":
	unittest.main() 
