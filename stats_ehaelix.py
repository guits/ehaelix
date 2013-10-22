#!/usr/bin/python

import os
import subprocess
import sys

def exec_command_by_ssh(host, command):
	process = subprocess.Popen("ssh %s '%s'" % (host, command), stdout=subprocess.PIPE, stderr=None, shell=True)                                                                                                                                                          
	output = process.communicate()
	return output[0].split()

test = exec_command_by_ssh("remy-web1.ext.hosting.enovance.com", "ls /home")
print test
