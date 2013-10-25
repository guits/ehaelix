#!/usr/bin/python

import os
import subprocess
import sys

class Cmd(object):
    def __init__(self, host):
        self._host = host

    def exec_command_host(self, command):
        process = subprocess.Popen("ssh %s '%s'" % (self._host, command), stdout=subprocess.PIPE, stderr=None, shell=True) 
        output = process.communicate()
    
        return [ line for line in output[0].split("\n") if line != '' ]

    def exec_command_on_vz(self, vz_id, command):
    #	print "ssh %s \"vzctl exec %s \\\"%s\\\"\"" % (host, vz_id, command)
        process = subprocess.Popen(r'ssh %s "vzctl exec %s \"%s\""' % (self._host, vz_id, command), stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()
        return [ line for line in output[0].split("\n") if line != '' ]


class Ehaelix(object):
    def __init__(self, host):
        self._host = host
        self._cmd = Cmd(self._host)

    def get_vz_list(self):
        vzlist_raw = self._cmd.exec_command_host("vzlist -a -H -o ctid,hostname,status")
        vzlist = []
        for vz in vzlist_raw:
            vzinfo = vz.split()
            if not vzinfo: continue
            vzlist.append({
    			'id': vzinfo[0],
    			'hostname': vzinfo[1],
    			'status': vzinfo[2],
    			'physical_host': self._host,
    			})
        return vzlist
    
    def get_cpu_info_vz(vz_id):
        command = "grep 'cpu MHz' /proc/cpuinfo"
        cpus = self._cmd.exec_command_on_vz(vz_id, command)
        cpu = cpus.pop().split()
        result = {
            'nb': len(cpus),
            'mhz': cpu[3],
            'unit': cpu[1],
        }
        return result
    
    def get_total_mem_info_vz(vz_id):
        command = "grep 'MemTotal' /proc/meminfo"
        infos = self._cmd.exec_command_on_vz(vz_id, command)
        info = infos.pop().split()
        result = {
            'name': info[0],
            'size': info[1],
            'unit': info[2],
        }
        return result
    
    def get_vgs_infos():
        lines_raw = self._cmd.exec_command_host("vgs")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'name': lineinfo[0],
                'size': lineinfo[5],
                'free': lineinfo[6],
            })
        return result
    
    def get_lvs_infos():
        lines_raw = self._cmd.exec_command_host("lvs")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'name': lineinfo[0],
                'vg': lineinfo[1],
                'size': lineinfo[3],
            })
        return result
    
    def get_mount_infos():
        lines_raw = self._cmd.exec_command_host("mount")
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'mount': lineinfo[2],
                'type': lineinfo[4],
            })
        return result
    
    def get_df_infos():
        lines_raw = self._cmd.exec_command_host("df -hP")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'size': lineinfo[1],
                'used': lineinfo[2],
                'available': lineinfo[3],
                'use%': lineinfo[4],
                'mount': lineinfo[5],
            })
        return result
    
    def get_df_vz_infos(vz_id):
        lines_raw = self._cmd.exec_command_on_vz(vz_id, "df -hP")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'size': lineinfo[1],
                'used': lineinfo[2],
                'available': lineinfo[3],
                'use%': lineinfo[4],
                'mount': lineinfo[5],
            })
        return result

srv = Ehaelix("eno-eh9-b2.mut-8.hosting.enovance.com")

vzlist = srv.get_vz_list()
print vzlist

#for vz in vzlist:
#    cpuinfo = get_cpu_info_vz(vz['id'])
#    totalmem = get_total_mem_info_vz(vz['id'])
#    print vz['hostname']
#    print "\tCPUs: %s (%s %s)\n\tTotal Ram: %s" % (cpuinfo['nb'], cpuinfo['mhz'],
#                                                  cpuinfo['unit'], totalmem['size'])
