#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import os
import re
from os.path import join, basename
import pygal


def ensure_float(str_number):
    return float(str_number.replace(',', '.'))


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
    if not os.path.isdir(os.path.dirname(final_dest_file)):
        os.makedirs(os.path.dirname(final_dest_file))
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
    chart.x_labels = ['socle', 'vzs']
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
    vg = info['socle']['vgs'][0]
    # Remove the forced G unit in lvs and vgs
    chart.add('Free', ensure_float(re.sub(r'G$', r'', vg['free'])))
    for lv in info['socle']['lvs']:
        if lv['vg'] == vg['name']:
            # get vz name by drbd mount_point
            # Print only mounted (primary drbd)
            drbd_mount_point = get_mounted_dir_for_device(info, lv['name'])
            if drbd_mount_point:
                chart.add(drbd_mount_point, ensure_float(re.sub(r'G$', r'',
                          lv['size'])))
    chart.render_to_file(final_dest_file)


def gen_disks_stacked_chart(info, dest_file, docs_dir='./docs', dry_run=False):
    final_dest_file = join(docs_dir, dest_file)
    if dry_run:
        print 'Generate graph StackedBar in %s' % final_dest_file
        return
    # Gen chart
    chart = pygal.StackedBar()
    chart.title = 'Disk space Assignement on %s (in G)' % info['socle']['name']
    chart.x_labels = ['Total', 'partitions']
    # Get only the first vs
    vg = info['socle']['vgs'][0]
    # Remove the forced G unit in lvs and vgs
    free_size = remove_exponent(vg['free'])
    chart.add('Free', [free_size, free_size])
    chart.add('Used', [remove_exponent(vg['size']) - free_size, None])
    other_size = 0
    for lv in info['socle']['lvs']:
        if lv['vg'] == vg['name']:
            # get vz name by drbd mount_point
            # Print only mounted (primary drbd)
            drbd_mount_point = get_mounted_dir_for_device(info, lv['name'])
            if drbd_mount_point:
                chart.add(drbd_mount_point, [None,
                          remove_exponent(lv['size'])])
            else:
                other_size += remove_exponent(lv['size'])

    # Add size of unmounted devices
    chart.add('Other', [None, other_size])

    chart.render_to_file(final_dest_file)


def gen_mem_stacked_chart(info, dest_file, docs_dir='./docs', dry_run=False):
    final_dest_file = join(docs_dir, dest_file)
    if dry_run:
        print 'Generate graph StackedBar in %s' % final_dest_file
        return
    # Gen chart
    chart = pygal.StackedBar()
    chart.title = 'Mem Assignement on %s in G' % info['socle']['name']
    chart.x_labels = ['socle', 'vzs']
    chart.add(info['socle']['name'],
              [int(info['socle']['ram']['size'])/1024/1024, None])
    for vz in info['vzs']:
        chart.add(vz['hostname'],
                  [None, int(vz['ram']['size'])/1024/1024])
    chart.render_to_file(final_dest_file)


def get_mounted_dir_for_device(info, device):
    device = re.sub('^lv_', '', device)
    drbd_device = info['socle']['drbd_overview'].get(device, {})
    return basename(drbd_device.get('mount_point', ''))


def remove_exponent(value, exponent='G'):
    "Remove exponent and return float"
    return ensure_float(re.sub(r'%s$' % exponent, r'', value))


def filter_name(name):
    "Return filter name without special chars for latex image name"
    return re.sub(r'[^a-zA-Z0-9]', '_', name)
