#!/usr/bin/python3

# This implementation of logread has almost the same behavior as
# the tail -F shell command, without needing tail.
# Current "Bug?": it reads and processes the whole file, in the future it
# should only process new lines written to the logfile, skipping the old lines.

def logread(logfilepath):
	with open(logfilepath) as logfile:
		while True: # Run until program exits
			line = logfile.readline()
			if line:
				print(line)
