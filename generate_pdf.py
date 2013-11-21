from jinja2 import Environment, FileSystemLoader
import os


TEMPLATE_DIR='./templates'
DOCS_DIR='./docs'


env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


filename = 'vz/101.rst'
template = env.get_template(filename)

class Link(object):
    href = None
    caption = None
    def __init__(self):
        pass

link = Link()
link.href = 'Link'
link.caption = 'Link name'
navigation = [link]
context = {'a_variable': 'Un truc', 'navigation': navigation}

print '----- %s in %s' % (os.path.basename(filename) ,os.path.dirname(filename))
print template.render(context)
#template.stream(context).dump( '%s/%s' % (DOCS_DIR, filename))

