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
PARSER.add_argument("-d", "--dry-run",
            help="Dry-run mode", action='store_true', default=False)
ARGS = PARSER.parse_args()

def get_all_infos(socle):
    # Render all VZ
    infos={}

    srv = Ehaelix(socle)
    vzs = srv.get_vz_list()
    infos['vzs'] = []
    for vz in vzs:
        vz['ram'] = srv.get_total_mem_info_vz(vz['id'])
        vz['os'] = srv.get_vz_os_version(vz['id'])
        vz['cpu'] = srv.get_cpu_info_vz(vz['id'])
        vz['disks'] = srv.get_df_vz_infos(vz['id'])
        vz['apps'] = srv.get_vz_list_apps(vz['id'])
        infos['vzs'].append(vz)
    
    # Render Physical host
    physical = {
        'name':  socle,
        'os':    srv.get_os_version(),
        'cpu':   srv.get_cpu_info(),
        'ram':   srv.get_total_mem_info(),
        'vgs':   srv.get_vgs_infos(),
        'lvs':   srv.get_lvs_infos(),
        'mount': srv.get_mount_infos(),
        'disks': srv.get_df_infos(),
    }

    infos['socle'] = physical
    return infos

INFOS={}

# Get all infos for b1
INFOS[ARGS.b1] = get_all_infos(ARGS.b1)
if ARGS.b2:
    INFOS[ARGS.b2] = get_all_infos(ARGS.b2)

# Render all
for cluster, info in INFOS.iteritems():
    # Render socle
    render(template='physical/physical.rst', dest_file='physical/%s.rst' % cluster,
           context={'PHYSICAL': info['socle']}, dry_run=ARGS.dry_run)
    # Render vz
    for vz in info['vzs']:
        render(template='vz/vz.rst', dest_file='vz/%s.rst' % vz['id'],
               context={'VZ':vz}, dry_run=ARGS.dry_run)

# Render 'index' page
render('index.rst', context={'INFOS': INFOS}, dry_run=ARGS.dry_run)






