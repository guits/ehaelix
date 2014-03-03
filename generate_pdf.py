#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import argparse
import os

from stats_ehaelix import Ehaelix

# Config
TEMPLATE_DIR = './templates'
DOCS_DIR = './docs'

# Get args
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-1", "--b1",
            help="Address of the host (B1)", type=str, required=True)
PARSER.add_argument("-2", "--b2",
            help="Address of the second host (B2)", type=str)
ARGS = PARSER.parse_args()

ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render(template, destfile=None, context={}, dry_run=False):
    """
    render function
    """
    if destfile:
        filename = destfile
    else:
        filename = template
    template = ENV.get_template(filename)
    try:
        if dry_run:
            print template.render(context)
        else:
            # Make needed directory
            print '----- %s in %s' % (os.path.basename(filename),
                                      os.path.dirname(filename))
            # Generate File
            template.stream(context).dump( '%s/%s' % (DOCS_DIR, filename))
    except UndefinedError as error:
        print 'Generate template %s error var : %s' % (filename, error)

# Render all VZ
SRV = Ehaelix(ARGS.b1)
VZS = SRV.get_vz_list()
PHYSICAL = {}
for vz in VZS:
    vz['ram'] = SRV.get_total_mem_info_vz(vz['id'])
    vz['cpu'] = SRV.get_cpu_info_vz(vz['id'])
    vz['disks'] = SRV.get_df_vz_infos(vz['id'])
    vz['apps'] = SRV.get_vz_list_apps(vz['id'])
    render('vz/vz.rst', context={'VZ':vz}, dry_run=True)

# Render Physical host
PHYSICAL['name'] = ARGS.b1
PHYSICAL['cpu'] = SRV.get_cpu_info()
PHYSICAL['ram'] = SRV.get_total_mem_info()
PHYSICAL['vgs'] = SRV.get_vgs_infos()
PHYSICAL['lvs'] = SRV.get_lvs_infos()
PHYSICAL['mount'] = SRV.get_mount_infos()
PHYSICAL['disks'] = SRV.get_df_infos()
print PHYSICAL
render('physical/physical.rst', context={'PHYSICAL':PHYSICAL}, dry_run=True)
