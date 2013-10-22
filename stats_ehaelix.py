#!/usr/bin/python

import os
import subprocess
import sys

host = "eno-eh9-b2.mut-8.hosting.enovance.com"

def exec_command_by_ssh(host, command):
	process = subprocess.Popen("ssh %s '%s'" % (host, command), stdout=subprocess.PIPE, stderr=None, shell=True)                                                                                                                                                          
	output = process.communicate()
	return output[0].split()

def get_vz_list(host):
	vzlist = exec_command_by_ssh(host, "vzlist -a")
	return vzlist

test = get_vz_list(host)
print test
