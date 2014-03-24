#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import argparse
import os
from tools import render

from stats_ehaelix import Ehaelix

# Get args
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-1", "--b1",
            help="Address of the host (B1)", type=str, required=True)
PARSER.add_argument("-2", "--b2",
            help="Address of the second host (B2)", type=str)
ARGS = PARSER.parse_args()

# Render all VZ
SRV = Ehaelix(ARGS.b1)
VZS = SRV.get_vz_list()
PHYSICAL = {}
INCLUDE = {}
INCLUDE['vzs'] = []
for vz in VZS:
    vz['ram'] = SRV.get_total_mem_info_vz(vz['id'])
    vz['cpu'] = SRV.get_cpu_info_vz(vz['id'])
    vz['disks'] = SRV.get_df_vz_infos(vz['id'])
    vz['apps'] = SRV.get_vz_list_apps(vz['id'])
    INCLUDE['vzs'].append(vz['id'])
    render(template='vz/vz.rst', destfile='vz/%s.rst' % vz['id'],
           context={'VZ':vz}, dry_run=True)

# Render Physical host
PHYSICAL['name'] = ARGS.b1
PHYSICAL['cpu'] = SRV.get_cpu_info()
PHYSICAL['ram'] = SRV.get_total_mem_info()
PHYSICAL['vgs'] = SRV.get_vgs_infos()
PHYSICAL['lvs'] = SRV.get_lvs_infos()
PHYSICAL['mount'] = SRV.get_mount_infos()
PHYSICAL['disks'] = SRV.get_df_infos()
INCLUDE['socle'] = []
INCLUDE['socle'].append(PHYSICAL['name'])
render('physical/physical.rst', context={'PHYSICAL':PHYSICAL}, dry_run=True)

# Render 'index' page
render('index/index.rst', context={'INCLUDE':INCLUDE}, dry_run=True)
