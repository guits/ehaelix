#!/usr/bin/python

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import os


def render(template, destfile=None, context={}, template_dir='./templates',
           docs_dir='./docs', dry_run=False):
    """
    render function
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    if not destfile:
        destfile = template

    template = env.get_template(template)
    print '----- %s in %s' % (os.path.basename(destfile),
                              os.path.dirname(destfile))
    try:
        if dry_run:
            print template.render(context)
        else:
            # TODO Make needed directory
            # Generate File
            template.stream(context).dump( '%s/%s' % (docs_dir, destfile))
    except UndefinedError as error:
        print 'Generate template %s error var : %s' % (destfile, error)
