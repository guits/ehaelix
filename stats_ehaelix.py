"""
Classe eHaelix
"""
#!/usr/bin/python

import subprocess
import re


class Cmd(object):
    """
    Class for execute via ssh a command
    """
    def __init__(self, host, apps_filter="mysql"):
        self._host = host
        self._apps_filter = apps_filter

    def exec_command_host(self, command):
        """
        Exec a command on a physical host
        """
        process = subprocess.Popen("ssh %s '%s'" % (self._host, command),
                                   stdout=subprocess.PIPE,
                                   stderr=None, shell=True)
        output = process.communicate()

        return [line for line in output[0].split("\n") if line != '']

    def exec_command_on_vz(self, vz_id, command):
        """
        Exec a command on a VZ
        """
    #	print "ssh %s \"vzctl exec %s \\\"%s\\\"\"" % (host, vz_id, command)
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

    def get_cpu_info_vz(self, vz_id):
        """
        Return CPU info of a VZ
        """
        command = "grep 'cpu MHz' /proc/cpuinfo"
        cpus = self._cmd.exec_command_on_vz(vz_id, command)
        cpu = cpus.pop().split()
        result = {
            'nb': len(cpus),
            'mhz': cpu[3],
            'unit': cpu[1],
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
        lines_raw = self._cmd.exec_command_host("vgs")
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
        lines_raw = self._cmd.exec_command_host("lvs")
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
                'use%': lineinfo[4],
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

    def get_vz_list_apps(self, vz_id, apps=["apache2", "tomcat[0-9]",
                                            "postgres",
                                            "mysql-server",
                                            r"mariadb-server-[0-9]\.[0-9]",
                                            "nginx", "varnish", "mongodb",
                                            "php5-fpm", "php5"]):
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


SRV = Ehaelix("eno-eh9-b2.mut-8.hosting.enovance.com")

VZLIST = SRV.get_vz_list()
for vz in VZLIST:
    print vz['hostname']
    vzapps = SRV.get_vz_list_apps(vz['id'])
    print vzapps
    for name, vzapp in vzapps.iteritems():
        print "name: %s\t\tversion: %s" % (vzapp['name'], vzapp['version'])
