.. _{{ PHYSICAL.name }}:

{{ PHYSICAL.name }}
------------
  * Hostname : {{ PHYSICAL.name }}
  * Cpu infos : {{ PHYSICAL.cpu.nb }} @ {{ PHYSICAL.cpu.mhz }} {{ PHYSICAL.cpu.unit }}
  * Mem infos : {{ PHYSICAL.ram.size }} {{ PHYSICAL.ram.unit }}
  * Disk Space :
    {% for disk in PHYSICAL.disks -%}
        {{ disk.device }} mounted on {{ disk.mount }} {{ disk.used }} / {{ disk.size }} {{ disk.use_p }}
    {% endfor %}
