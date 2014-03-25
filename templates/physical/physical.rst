.. _{{ PHYSICAL.name }}:

{{ PHYSICAL.name }}
-------------------------------

  * **Hostname** : {{ PHYSICAL.name }}
  * **Cpu** : {{ PHYSICAL.cpu.nb }} X {{ PHYSICAL.cpu.mhz }} {{ PHYSICAL.cpu.unit }}
  * **Memory** : {{ PHYSICAL.ram.size }} {{ PHYSICAL.ram.unit }}
  * **OS version** : {{ PHYSICAL.os }}
  * **Drbd** :
      * VGs:
      {%- for vg in PHYSICAL.vgs %}
          * {{ vg.name }}
          * size: {{ vg.size }}
          * free: {{ vg.free }}
          * LVs:
          {%- for lv in PHYSICAL.lvs %}
          {%- if lv.vg == vg.name %}
              * {{ lv.name }} size: {{ lv.size }}
          {%- endif %}
          {%- endfor %}
      {%- endfor %}
  * **Disk Space** :
      {%- for disk in PHYSICAL.disks %}
          * {{ disk.device }} mounted on {{ disk.mount }} {{ disk.used }} / {{ disk.size }} {{ disk.use_p }}
      {%- endfor %}
