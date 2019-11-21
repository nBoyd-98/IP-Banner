#!/usr/bin/env python3

from DatabaseHelper import *
from Server import *

def main():
	db = DatabaseHelper()
	server = Server("test", "test", "test", "test")
	blacklist = db.add_blacklist(server, "1.1.1.1")


if __name__ == "__main__":
	main()
