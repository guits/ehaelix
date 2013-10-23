#!/usr/bin/python

import os
import subprocess
import sys

host = "eno-eh9-b2.mut-8.hosting.enovance.com"

def exec_command_host(host, command):
    process = subprocess.Popen("ssh %s '%s'" % (host, command), stdout=subprocess.PIPE, stderr=None, shell=True) 
    output = process.communicate()

    return [ line for line in output[0].split("\n") if line != '' ]

def exec_command_on_vz(host, vz_id, command):
#	print "ssh %s \"vzctl exec %s \\\"%s\\\"\"" % (host, vz_id, command)
    process = subprocess.Popen(r'ssh %s "vzctl exec %s \"%s\""' % (host, vz_id, command), stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    return [ line for line in output[0].split("\n") if line != '' ]

def get_vz_list(host):
    vzlist_raw = exec_command_host(host, "vzlist -a -H -o ctid,hostname,status")
    vzlist = []
    for vz in vzlist_raw:
        vzinfo = vz.split()
        if not vzinfo: continue
        vzlist.append({
			'id': vzinfo[0],
			'hostname': vzinfo[1],
			'status': vzinfo[2],
			'physical_host': host,
			})
    return vzlist

def get_cpu_info_vz(vz_id):
    command = "grep 'cpu MHz' /proc/cpuinfo"
    cpus = exec_command_on_vz(vz['physical_host'], vz_id, command)
    cpu = cpus.pop().split()
    result = {
        'nb': len(cpus),
        'mhz': cpu[3],
        'unit': cpu[1],
    }
    return result

def get_total_mem_info_vz(vz_id):
    command = "grep 'MemTotal' /proc/meminfo"
    infos = exec_command_on_vz(vz['physical_host'], vz_id, command)
    info = infos.pop().split()
    result = {
        'name': info[0],
        'size': info[1],
        'unit': info[2],
    }
    return result

def get_vgs_infos(host):
    lines_raw = exec_command_host(host, "vgs")
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

def get_lvs_infos(host):
    lines_raw = exec_command_host(host, "lvs")
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

def get_mount_infos(host):
    lines_raw = exec_command_host(host, "mount")
    result = []
    for line in lines_raw:
        lineinfo = line.split()
        result.append({
            'device': lineinfo[0],
            'mount': lineinfo[2],
            'type': lineinfo[4],
        })
    return result

def get_df_infos(host):
    lines_raw = exec_command_host(host, "df -hP")
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

def get_df_vz_infos(host, vz_id):
    lines_raw = exec_command_on_vz(host, vz_id, "df -hP")
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


vzlist = get_vz_list(host)

print(get_df_vz_infos(host, "102"))

#for vz in vzlist:
#    cpuinfo = get_cpu_info_vz(vz['id'])
#    totalmem = get_total_mem_info_vz(vz['id'])
#    print vz['hostname']
#    print "\tCPUs: %s (%s %s)\n\tTotal Ram: %s" % (cpuinfo['nb'], cpuinfo['mhz'],
#                                                  cpuinfo['unit'], totalmem['size'])
