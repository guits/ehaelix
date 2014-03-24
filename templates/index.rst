.. Rapport documentation master file, created by
   sphinx-quickstart on Wed Oct 23 23:56:06 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rapport cluster ehaelix
=========================

Contents:

.. toctree::
   :maxdepth: 2

{% for cluster, info in INFOS.iteritems() -%}
    physical/{{ info.socle.name }}.rst
{% for vz in info.vzs -%}
    vz/{{ vz.id }}.rst
{% endfor %}
{% endfor %}




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

