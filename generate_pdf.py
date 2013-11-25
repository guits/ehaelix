from jinja2 import Environment, FileSystemLoader
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




# Tests :
SRV = Ehaelix(ARGS.b1)
VZ = SRV.get_vz_list().pop()



env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

filename = 'vz/vz.rst'
template = env.get_template(filename)

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

context = {'VZ': VZ}

print '----- %s in %s' % (os.path.basename(filename) ,os.path.dirname(filename))
print template.render(context)
#template.stream(context).dump( '%s/%s' % (DOCS_DIR, filename))

