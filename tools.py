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
    if destfile:
        filename = destfile
    else:
        filename = template
    template = env.get_template(filename)
    try:
        if dry_run:
            print template.render(context)
        else:
            # Make needed directory
            print '----- %s in %s' % (os.path.basename(filename),
                                      os.path.dirname(filename))
            # Generate File
            template.stream(context).dump( '%s/%s' % (docs_dir, filename))
    except UndefinedError as error:
        print 'Generate template %s error var : %s' % (filename, error)
