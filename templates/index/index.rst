{% for s in INCLUDE.socle -%}
.. include:: physical/{{ s }}.rst
-------
{% endfor %}
{% for vz in INCLUDE.vzs -%}
.. include:: vz/{{ vz }}.rst
--------
{% endfor %}
