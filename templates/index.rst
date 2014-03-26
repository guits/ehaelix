.. Rapport documentation master file, created by
   sphinx-quickstart on Wed Oct 23 23:56:06 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rapport cluster ehaelix
=========================

Contents:

.. toctree::
    :maxdepth: 2
{% for cluster, info in INFOS.iteritems() %}
    physical/{{ info.socle.name }}.rst
{%- for vz in info.vzs %}
    vz/{{ vz.id }}.rst
{%- endfor %}
{%- endfor %}



Liste des environnements dans le cluster
==========================================

{% for cluster, info in INFOS.iteritems() %}
    * **{{ info.socle.name }}**
{%- for vz in info.vzs %}
        * {{ vz.hostname }}
{%- endfor %}
{%- endfor %}


Charts
========

Cpu
----

{% for cluster, info in INFOS.iteritems() %}
.. image:: physical/cpus_{{ info.socle.name }}.svg
    :width: 800px
    :height: 500px
{% endfor %}

{% for cluster, info in INFOS.iteritems() %}
.. image:: physical/cpus_stacked_{{ info.socle.name }}.svg
    :width: 800px
    :height: 500px
{% endfor %}

Disk
-----

{% for cluster, info in INFOS.iteritems() %}
.. image:: physical/disks_{{ info.socle.name }}.svg
    :width: 800px
    :height: 500px
{% endfor %}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

