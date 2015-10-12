"""
Class eHaelix
"""
#!/usr/bin/python

import subprocess
import re
from jinja2 import Template, Environment, PackageLoader, FileSystemLoader


class Cmd(object):
    """
    Class for execute via ssh a command
    """
    def __init__(self, host):
        self._host = host

    def exec_command_host(self, command):
        """
        Exec a command on a physical host
        """
        process = subprocess.Popen(r'ssh %s "%s"' % (self._host, command),
                                   stdout=subprocess.PIPE,
                                   stderr=None, shell=True)
        output = process.communicate()

        return [line for line in output[0].split("\n") if line != '']

    def exec_command_on_vz(self, vz_id, command):
        """
        Exec a command on a VZ
        """
        process = subprocess.Popen(r'ssh %s "vzctl exec %s \"%s\""' %
                                   (self._host, vz_id, command),
                                   stdout=subprocess.PIPE,
                                   stderr=None,
                                   shell=True)
        output = process.communicate()
        return [line for line in output[0].split("\n") if line != '']


class Ehaelix(object):
    """
    Class for get several information about an eHaelix cluster
    """
    def __init__(self, host):
        self._host = host
        self._cmd = Cmd(self._host)

    def get_drbd_overview(self):
        """
        Return get drbd-overview infos
        """
        drbd_overview = {}
        fields_name = [
            'id_name',
            'connection_state',
            'role',
            'disk_states',
            'replication_protocol',
            'io_flags',
            'mount_point',
            'filesystem',
            'size',
            'free',
            'used',
            'percent',
        ]
        for line in self._cmd.exec_command_host('drbd-overview'):
            _drbd_line = {}
            for index, field in enumerate(line.split()):
                _drbd_line[fields_name[index]] = field
            # Get only name
            drbd_name = _drbd_line['id_name'].split(':')[1]
            drbd_overview[drbd_name] = _drbd_line
        return drbd_overview

    def get_vz_list(self):
        """
        Return the VZ list of a physical host
        """
        vzlist_raw = self._cmd.exec_command_host(
            "vzlist -a -H -o ctid,hostname,status")
        vztab = []
        for vz in vzlist_raw:
            vzinfo = vz.split()
            if not vzinfo:
                continue
            vztab.append({
                'id': vzinfo[0],
                'hostname': vzinfo[1],
                'status': vzinfo[2],
                'physical_host': self._host,
            })
        return vztab

    def get_cpu_info(self):
            """
            Return CPU info of a physical machine
            """
            command = "grep 'cpu MHz' /proc/cpuinfo"
            #print command
            cpus = self._cmd.exec_command_host(command)
            cpu = cpus.pop().split()
            result = {
                'nb': len(cpus) + 1,
                'mhz': cpu[3],
                'unit': cpu[1],
            }
            return result

    def get_cpu_info_vz(self, vz_id):
        """
        Return CPU info of a VZ
        """
        command = "grep 'cpu MHz' /proc/cpuinfo"
        cpus = self._cmd.exec_command_on_vz(vz_id, command)
        cpu = cpus.pop().split()
        result = {
            'nb': len(cpus) + 1,
            'mhz': cpu[3],
            'unit': cpu[1],
        }
        return result

    def get_total_mem_info(self):
        """
        Return memory info of a physical machine
        """
        command = "grep 'MemTotal' /proc/meminfo"
        infos = self._cmd.exec_command_host(command)
        info = infos.pop().split()
        result = {
            'name': info[0],
            'size': info[1],
            'unit': info[2],
        }
        return result

    def get_total_mem_info_vz(self, vz_id):
        """
        Return memory info of a VZ
        """
        command = "grep 'MemTotal' /proc/meminfo"
        infos = self._cmd.exec_command_on_vz(vz_id, command)
        info = infos.pop().split()
        result = {
            'name': info[0],
            'size': info[1],
            'unit': info[2],
        }
        return result

    def get_vgs_infos(self):
        """
        Return informations about VGs on a physical host
        """
        lines_raw = self._cmd.exec_command_host("vgs --units G")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'name': lineinfo[0],
                'size': lineinfo[5],
                'free': lineinfo[6],
            })
        return result

    def get_lvs_infos(self):
        """
        Return informations about LVs on a physicial host
        """
        lines_raw = self._cmd.exec_command_host("lvs --units G")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'name': lineinfo[0],
                'vg': lineinfo[1],
                'size': lineinfo[3],
            })
        return result

    def get_mount_infos(self):
        """
        Return mount information on a physical host
        """
        lines_raw = self._cmd.exec_command_host("mount")
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'mount': lineinfo[2],
                'type': lineinfo[4],
            })
        return result

    def get_hw_model(self):
        """
        Return hw model
        """
        lines_raw = self._cmd.exec_command_host('dmidecode -s system-manufacturer'
                                           ' && dmidecode -s system-product-name')

        # One result by line so get therse lines content
        result = {
            'manufacturer': lines_raw[0].rstrip('\n'),
            'product': lines_raw[1].rstrip('\n'),
        }
        return result

    def get_kernel_version(self):
        """
        Return kernel version
        """
        lines_raw = self._cmd.exec_command_host('uname -r')
        return lines_raw.pop().rstrip('\n')

    def get_os_version(self):
        """
        Return Operating system version (little debian friendly)
        """
        lines_raw = self._cmd.exec_command_host('cat /etc/issue.net')
        return lines_raw.pop().rstrip('\n')

    def get_vz_os_version(self, vz_id):
        """
        Return Operating system version (little debian friendly)
        """
        lines_raw = self._cmd.exec_command_on_vz(vz_id, 'cat /etc/issue.net')
        return lines_raw.pop().rstrip('\n')

    def get_df_infos(self):
        """
        Return space disk information on a physical host
        """
        lines_raw = self._cmd.exec_command_host("df -hP")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'size': lineinfo[1],
                'used': lineinfo[2],
                'available': lineinfo[3],
                'used_p': lineinfo[4],
                'mount': lineinfo[5],
            })
        return result

    def get_df_vz_infos(self, vz_id):
        """
        Return disk space informations of a VZ
        """
        lines_raw = self._cmd.exec_command_on_vz(vz_id, "df -hP")
        # delete first line
        lines_raw = lines_raw[1:]
        result = []
        for line in lines_raw:
            lineinfo = line.split()
            result.append({
                'device': lineinfo[0],
                'size': lineinfo[1],
                'used': lineinfo[2],
                'available': lineinfo[3],
                'use%': lineinfo[4],
                'mount': lineinfo[5],
            })
        return result

    def get_vz_list_apps(self, vz_id, apps=[
                                "apache2-mpm-.*",
                                "nginx",
                                "tomcat[0-9]",
                                "varnish",
                                "postgresql-[0-9]\.[0-9]",
                                "mysql-server",
                                r"mariadb-server-[0-9]\.[0-9]",
                                "mongodb",
                                "php5-fpm", "php5", "zend-server-.*-php.*"]):
        """
        Return an array of apps listed in 'apps' arg,
        with status and version number
        """
        command = "dpkg -l"
        lines_raw = self._cmd.exec_command_on_vz(vz_id, command)
        result = {}
        for line in lines_raw:
            lineinfo = line.split()
            if len(lineinfo) >= 3:
                for app in apps:
                    regexp = "^%s$" % (app)
                    match = re.match(regexp, lineinfo[1])
                    if match:
                        result[lineinfo[1]] = {
                            'name': lineinfo[1],
                            'status': lineinfo[0],
                            'version': lineinfo[2],
                        }
        return result


#SRV = Ehaelix("eno-eh9-b2.mut-8.hosting.enovance.com")
#print SRV.get_cpu_info()
#templateLoader = FileSystemLoader( searchpath="./" )
#templateEnv = Environment( loader=templateLoader )
#TEMPLATE_FILE = "./templates/report.rst"
#template = templateEnv.get_template( TEMPLATE_FILE )
#outputText = template.render()

#
#VZLIST = SRV.get_vz_list()
#for vz in VZLIST:
#    print vz['hostname']
#    vzapps = SRV.get_vz_list_apps(vz['id'])
#    print vzapps
#    for name, vzapp in vzapps.iteritems():
#        print "name: %s\t\tversion: %s" % (vzapp['name'], vzapp['version'])
