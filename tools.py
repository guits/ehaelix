#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import os
import re
from os.path import join, basename
import pygal


def render(template, dest_file=None, context={}, template_dir='./templates',
           docs_dir='./docs', dry_run=False):
    """
    render function
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    if not dest_file:
        dest_file = template

    template = env.get_template(template)
    print '----- %s in %s' % (os.path.basename(dest_file),
                              os.path.dirname(dest_file))
    try:
        if dry_run:
            print template.render(context)
        else:
            dest_dir = os.path.dirname(dest_file)
            final_dest_dir = join(docs_dir, dest_dir)
            final_dest_file = join(docs_dir, dest_file)
            if not os.path.isdir(final_dest_dir):
                os.makedirs(final_dest_dir)
            # Generate File
            template.stream(context).dump(final_dest_file)
    except UndefinedError as error:
        print 'Generate template %s error var : %s' % (dest_file, error)


def gen_cpus_chart(info, dest_file, docs_dir='./docs', dry_run=False):
    final_dest_file = join(docs_dir, dest_file)
    if dry_run:
        print 'Generate graph HorizontalBar in %s' % final_dest_file
        return
    # Gen chart
    chart = pygal.HorizontalBar()
    chart.title = 'Cpus Assignement on %s' % info['socle']['name']
    chart.add(info['socle']['name'], info['socle']['cpu']['nb'])
    for vz in info['vzs']:
        chart.add(vz['hostname'], vz['cpu']['nb'])
    chart.render_to_file(final_dest_file)

def gen_cpus_stacked_chart(info, dest_file, docs_dir='./docs', dry_run=False):
    final_dest_file = join(docs_dir, dest_file)
    if dry_run:
        print 'Generate graph StackedBar in %s' % final_dest_file
        return
    # Gen chart
    chart = pygal.StackedBar()
    chart.title = 'Cpus Assignement on %s' % info['socle']['name']
    chart.x_labels = ['socle','vzs']
    chart.add(info['socle']['name'], [info['socle']['cpu']['nb'], None])
    for vz in info['vzs']:
        chart.add(vz['hostname'], [None, vz['cpu']['nb']])
    chart.render_to_file(final_dest_file)

def gen_disks_chart(info, dest_file, docs_dir='./docs', dry_run=False):
    final_dest_file = join(docs_dir, dest_file)
    if dry_run:
        print 'Generate graph Pie in %s' % final_dest_file
        return
    # Gen chart
    chart = pygal.Pie()
    chart.title = 'Disk space Assignement on %s' % info['socle']['name']
    # Get only the first vs
    vg = info['socle']['vgs'].pop()
    # Remove the forced G unit in lvs and vgs
    chart.add('Free', float(re.sub(r'G$', r'', vg['free'])))
    for lv in info['socle']['lvs']:
        if lv['vg'] == vg['name']:
            chart.add(lv['name'], float(re.sub(r'G$', r'', lv['size'])))
    chart.render_to_file(final_dest_file)


def get_mounted_dir_for_device(info, device):
    for disk in info['socle']['disks']:
        if disk['device'] == device:
            return basename(disk['mount'])
    return 'None'

