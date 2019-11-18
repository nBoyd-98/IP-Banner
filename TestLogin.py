#!/usr/bin/python3

import unittest

from IPBannerMain import *

class testLogin(unittest.TestCase):

	def test_login(self):
		LoginWindow()		
		self.assertTrue(myhelper.checkpassword(name, psw))

if __name__ == "__main__":
	unittest.main()
