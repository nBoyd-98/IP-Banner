#!/bin/sh

# Flush out and reapply list every refresh
ipfw -q -f flush

# Set ethernet interface name here
eth_if="wlp1s0"

ipfw -q add 134 deny tcp from 199.34.2.1 to me via $eth_if keep-state
ipfw -q add 4188 deny tcp from 167.23.4.3 to me via $eth_if keep-state
ipfw -q add 6387 deny tcp from 198.89.8.9 to me via $eth_if keep-state
ipfw -q add 3441 deny tcp from 222.76.5.4 to me via $eth_if keep-state
ipfw -q add 9844 deny tcp from 1.1.1.1 to me via $eth_if keep-state
ipfw -q add 6778 deny tcp from 66.66.67.7 to me via $eth_if keep-state
ipfw -q add 446 deny tcp from 33.45.5.3 to me via $eth_if keep-state
