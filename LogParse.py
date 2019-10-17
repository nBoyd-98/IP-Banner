#!/usr/bin/python3
import re


# This implementation of logread has almost the same behavior as
# the tail -F shell command, without needing tail.
# Current "Bug?": it reads and processes the whole file, in the future it
# should only process new lines written to the logfile, skipping the old lines.

def logread(logfilepath):
	with open(logfilepath) as logfile:
		while True: # Run until program exits
			line = logfile.readline()
			if line:
				match = re.search("sshd.*(Failed+|Unable+|not)", line)
				if (match):
					pull_ip(line)
					
				
def pull_ip(line):
	print(line)
	ipaddr = re.search("((?:[0-9]{1,3}\.){3}[0-9]{1,3})", line).group(1)
	print(ipaddr)


