.. _{{ VZ.id }}:

{{ VZ.id }}
------------
  * **Physical host** : {{ VZ.physical_host }}
  * **Hostname** : {{ VZ.hostname }}
  * **OS version** : {{ VZ.os }}
  * **Status** : {{ VZ.status }}
  * **Total memory** : {{ VZ.ram.size }} {{ VZ.ram.unit }}
  * **Cpu** : {{ VZ.cpu.nb }} X {{ VZ.cpu.mhz }} {{ VZ.cpu.unit }}
  * **Disk Space** :
  {%- for disk in VZ.disks %}
      * {{ disk.device }} mounted on {{ disk.mount }} {{ disk.used }} / {{ disk.size }} {{ disk.use_p }}
  {%- endfor %}
  * **Apps** :
  {%- for app,value in VZ.apps.iteritems() %}
      * {{ value.name }} {{ value.version }}
  {%- endfor %}
