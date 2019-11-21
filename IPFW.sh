#!/bin/sh

# Flush out and reapply list every refresh
ipfw -q -f flush

# Set ethernet interface name here
eth_if=""

