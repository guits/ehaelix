.. _{{ PHYSICAL.name }}:

Detail socle {{ PHYSICAL.name }}
=========================================

  * **Hostname** : {{ PHYSICAL.name }}
  * **Hardware** : {{ PHYSICAL.hardware.manufacturer }} {{ PHYSICAL.hardware.product }}
  * **Kernel** : {{ PHYSICAL.kernel }}
  * **Cpu** : {{ PHYSICAL.cpu.nb }} X {{ PHYSICAL.cpu.mhz }} {{ PHYSICAL.cpu.unit }}
  * **Memory** : {{ PHYSICAL.ram.size }} {{ PHYSICAL.ram.unit }}
  * **OS version** : {{ PHYSICAL.os }}
  * **VGs**:
  {%- for vg in PHYSICAL.vgs %}
      * {{ vg.name }} - free: {{ vg.free }} / {{ vg.size }}
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
  * **Environnements** :
      {%- for vz in VZS %}
          * {{ vz.id }} : {{ vz.hostname }}
              * cpu : {{ vz.cpu.nb }} x {{ vz.cpu.mhz }} {{ vz.cpu.unit }}
              * ram : {{ vz.ram.size }} {{ vz.ram.unit }}
                {#- 0 because the first if / #}
              * disk : {{ vz.disks[0].size }}
      {%- endfor %}

