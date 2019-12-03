#!/bin/sh

# Flush out and reapply list every refresh
ipfw -q -f flush

# Set ethernet interface name here
eth_if="wlp1s0"

# You need this rule or you get locked out
ipfw -q add 65500 allow all from any to any

