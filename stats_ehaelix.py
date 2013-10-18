#!/usr/bin/python

import os
import subprocess
import sys

def exec_command_by_ssh(host, command):
    subprocess.call(["ls"], "-l")
