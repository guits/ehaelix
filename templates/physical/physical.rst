.. _{{ PHYSICAL.name }}:

{{ PHYSICAL.name }}
------------
  * Hostname : {{ PHYSICAL.name }}
  * Cpu infos : {{ PHYSICAL.cpu.nb }} @ {{ PHYSICAL.cpu.mhz }} {{ PHYSICAL.cpu.unit }}
  * Mem infos : {{ PHYSICAL.ram.size }} {{ PHYSICAL.ram.unit }}
  * Drbd infos :
    VGs:
    {% for vg in PHYSICAL.vgs -%}
      {{ vg.name }}
          size: {{ vg.size }}
          free: {{ vg.free }}
          LVs:
          {% for lv in PHYSICAL.lvs -%}
          {% if lv.vg == vg.name -%}
                {{ lv.name }} size: {{ lv.size }}
          {% endif -%}
          {% endfor -%}
    {% endfor %}
  * Disk Space :
    {% for disk in PHYSICAL.disks -%}
        {{ disk.device }} mounted on {{ disk.mount }} {{ disk.used }} / {{ disk.size }} {{ disk.use_p }}
    {% endfor %}
