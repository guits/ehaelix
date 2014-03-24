#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import os
from os.path import join


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
