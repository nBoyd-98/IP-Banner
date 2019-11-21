#!/usr/bin/env python3

import unittest

from os import path
from sys import platform
from subprocess import check_output

class TestRequiredFiles(unittest.TestCase):
	def test_files_exist(self):
		current_OS = platform
		if current_OS == 'linux':
			try:
				if check_output(["pidof", "systemd"]) > 0:
					self.assertTrue(path.exists("/var/log/auth.log"))
					print("Auth File exists") # UGLY
			except:
				pass
			else :
				print("Running Systemd, file not required")
		elif current_OS == 'freebsd11' or current_OS == 'freebsd12':
			self.assertTrue(path.exists("/var/log/auth.log"))
		elif current_OS == 'netbsd8' or current_OS == 'netbsd9':
			self.assertTrue(path.exists("/var/log/authlog"))
		


if __name__ == "__main__":
	unittest.main()
	
