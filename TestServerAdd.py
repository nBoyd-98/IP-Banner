#!/usr/bin/env python3 

import unittest

from Server import *

class TestServerAdd(unittest.TestCase):

	def test_add(self):
		self.assertTrue(Server("testHost", "testUser", "testPass", "testNick"))

if __name__ == "__main__":
	unittest.main() 
