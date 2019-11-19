#!/bin/python3

import LogParse
import re
import subprocess
import random
import threading
import fileinput

# As of right now the sysadmin needs to create and configure
# a shell script to update the firewall rules, we will be modifying and
# running the script.  The script based approach is easier and we already
# have the required root access from reading the authlog.


# The FreeBSD firewall IPFW is currently used in this program but that will change to a vairable.
def ban_ip(ipaddr):
	# That should be big enough for no duplicates, otherwise we need incremental rule numbers *lame*
	rule_num = random.randint(20, 10001)
	with open("IPFW.sh", "a") as rulefile:
		rulefile.write("ipfw -q add " + rule_num + " deny tcp from " + ipaddr + " to me via $eth_if keep-state")

	subprocess.call(['sh IPFW.sh'])
	# Timer uses Magic Number 20 for the ban time, this should be a vairable soon.
	timer = threading.Timer(20.0, unban_ip, [rule_num])
	timer.start()

def unban_ip(rule_num):
	with fileinput.FileInput(IPFW.sh, inplace = True) as rulefile:
		for line in rulefile:
			if not re.search(rule_num, line):
				print(line,end='')


