from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError
import argparse
import os

from stats_ehaelix import Ehaelix

# Config
TEMPLATE_DIR='./templates'
DOCS_DIR='./docs'

# Get args
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-1", "--b1",
            help="Address of the host (B1)", type=str, required=True)
PARSER.add_argument("-2", "--b2",
            help="Address of the second host (B2)", type=str)
ARGS = PARSER.parse_args()

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render(filename, context={}, dry_run=False):
    template = env.get_template(filename)
    try:
        if dry_run:
            print template.render(context)
        else:
            # Make needed directory
            print '----- %s in %s' % (os.path.basename(filename) ,os.path.dirname(filename))
            # Generate File
            template.stream(context).dump( '%s/%s' % (DOCS_DIR, filename))
    except UndefinedError as e:
        print 'Generate template %s error var : %s' % (filename, e)

# Render all files
render('vz/vz.rst', dry_run=True)




# Tests :
# SRV = Ehaelix(ARGS.b1)
# VZ = SRV.get_vz_list().pop()




#filename = 'vz/vz.rst'
#template = env.get_template(filename)

#class Link(object):
#    href = None
#    caption = None
#    def __init__(self):
#        pass
#
#link = Link()
#link.href = 'Link'
#link.caption = 'Link name'
#navigation = [link]
#context = {'a_variable': 'Un truc', 'navigation': navigation}
#context = {'VZ': VZ}


