from apps.util.zabbix_client.zabbix_api_source.gather_monitor_data import ZabbixClient
from apps.util.zabbix_client.zabbix_api_source.gather_zabbix_image import ZabbixGraph
from apps.util.zabbix_client.zabbix_api_source.gather_monitor_data import graph_groups
import os

width = 900
image_files_dir = '/tmp/pngs/'

if not os.path.isdir(image_files_dir):
    os.makedirs(image_files_dir)


class ZabbixDataHandler(object):

    def __init__(self, **kwargs):
        self.zabbix_client = ZabbixClient(**kwargs)
        self.zabbix_graph = ZabbixGraph(kwargs.get('username'), kwargs.get('password'), kwargs.get('login_url'))
        self.graph_url = kwargs.get("graph_url")
        self.pie_graph_url = kwargs.get("pie_graph_url")

    def get_all_hosts(self):
        return self.zabbix_client.get_hosts()

    def get_all_data(self, curtime, period):
        hosts = self.zabbix_client.get_hosts()
        for host in hosts:
            general_view_list = ['Host name', 'Host boot time', 'CPU system time', 'CPU user time', 'CPU iowait time',
                                 'Processor load (15 min average per core)',
                                 'Processor load (1 min average per core)',
                                 'Processor load (5 min average per core)', 'Total memory', 'Available memory',
                                 'Total swap space', 'Free swap space', 'Total disk space on /',
                                 'Free disk space on /', 'Total disk space on /home', 'Free disk space on /home',
                                 'Number of running processes', 'Number of processes',
                                 'Total network incoming per second',
                                 "Total network outgoing per second",
                                 "Disk total read per second",
                                 "Disk total write per second", ]

            apps = self.zabbix_client.get_applications(host.get('hostid'))
            general_view = []
            for app in apps:
                items = self.zabbix_client.get_host_monitor_item_values_with_application(host.get('hostid'),
                                                                                         app.get('name'),
                                                                                         app.get('applicationid'))
                for i, item in enumerate(items):
                    if item.get('name') in general_view_list and app.get('name') not in ['General', 'Performance']:
                        general_view.append(item)
                for i, item in enumerate(items):
                    if item.get('name') in ['Total_network_outgoing', 'Total_network_incoming', 'Disk_total_read',
                                            'Disk_total_write']:
                        items.remove(items[i])
                app.update(items=items)
            host.update(general_view=general_view)
            host.update(applications=apps)
            graphs = self.get_host_graphs(curtime, period, **host)
            host.update(graphs=graphs)
        return hosts

    def graph_handler(self, hostid, hostname, curtime, period, **kwargs):
        if kwargs.get('graphtype') == '0' or kwargs.get('graphtype') == '1':
            return self.zabbix_graph.get_graph_chart2(image_files_dir,
                                                      self.graph_url,
                                                      hostid=hostid,
                                                      hostname=hostname,
                                                      graph_name=kwargs.get('name'),
                                                      graphid=kwargs.get('graphid'),
                                                      curtime=curtime,
                                                      period=period,
                                                      width=width
                                                      )
        elif kwargs.get('graphtype') == '2':
            return self.zabbix_graph.get_graph_chart6(image_files_dir,
                                                      self.pie_graph_url,
                                                      hostid=hostid,
                                                      hostname=hostname,
                                                      graph_name=kwargs.get('name'),
                                                      graphid=kwargs.get('graphid'),
                                                      curtime=curtime,
                                                      period=period,
                                                      )

    def get_host_graphs(self, curtime, period, **host):
        graphs = self.zabbix_client.get_host_graphids(host.get('hostid'))
        graphs_group = {
            'network': [],
            'rabbitmq': [],
            'redis': [],
            'memory': [],
            'raid': [],
            'swap': [],
            'mysql': [],
            'disk': [],
            'cpu': []
        }
        for g in graphs:
            images = self.graph_handler(host.get('hostid'), host.get('host'), curtime, period, **g)
            g.update(images=images)
            x = graph_groups(g.get("name"))[0]
            if x == 'network':
                graphs_group.get('network').append(g)
            elif x == 'redis':
                graphs_group.get('redis').append(g)
            elif x == 'rabbitmq':
                graphs_group.get('rabbitmq').append(g)
            elif x == 'memory':
                graphs_group.get('memory').append(g)
            elif x == 'raid':
                graphs_group.get('raid').append(g)
            elif x == 'swap':
                graphs_group.get('swap').append(g)
            elif x == 'mysql':
                graphs_group.get('mysql').append(g)
            elif x == 'disk':
                graphs_group.get('disk').append(g)
            elif x == 'cpu':
                graphs_group.get('cpu').append(g)
        return graphs_group

    def general_views(self, hostid):
        apps = self.zabbix_client.get_applications(hostid)
        general_view_list = ['Host name',
                             'Host boot time',
                             'CPU system time',
                             'CPU user time',
                             'CPU iowait time',
                             'Processor load (15 min average per core)',
                             'Processor load (1 min average per core)',
                             'Processor load (5 min average per core)',
                             'Total memory',
                             'Available memory',
                             'Total swap space', 'Free swap space',
                             'Total disk space on /',
                             'Free disk space on /',
                             'Total disk space on /home',
                             'Free disk space on /home',
                             'Number of running processes',
                             'Number of processes',
                             'Total network incoming per second',
                             "Total network outgoing per second",
                             "Disk total read per second",
                             "Disk total write per second", ]
        general_view = []
        for app in apps:
            items = self.zabbix_client.get_host_monitor_item_values_with_application(hostid,
                                                                                     app.get('name'),
                                                                                     app.get('applicationid'))
            for i, item in enumerate(items):
                if item.get('name') in general_view_list and app.get('name') != 'Performance':
                    general_view.append(item)
            for i, item in enumerate(items):
                if item.get('name') in ['Total_network_outgoing',
                                        'Total_network_incoming',
                                        'Disk_total_read',
                                        'Disk_total_write']:
                    items.remove(items[i])
        return general_view

    def get_host_data(self, hostid, curtime, period):
        host = self.zabbix_client.get_hosts(hostid)[0]
        general_view_list = ['Host name', 'Host boot time', 'CPU system time', 'CPU user time', 'CPU iowait time',
                             'Processor load (15 min average per core)',
                             'Processor load (1 min average per core)',
                             'Processor load (5 min average per core)', 'Total memory', 'Available memory',
                             'Total swap space', 'Free swap space', 'Total disk space on /',
                             'Free disk space on /', 'Total disk space on /home', 'Free disk space on /home',
                             'Number of running processes', 'Number of processes',
                             'Total network incoming per second',
                             "Total network outgoing per second",
                             "Disk total read per second",
                             "Disk total write per second", ]

        apps = self.zabbix_client.get_applications(host.get('hostid'))
        general_view = []
        for app in apps:
            items = self.zabbix_client.get_host_monitor_item_values_with_application(host.get('hostid'),
                                                                                     app.get('name'),
                                                                                     app.get('applicationid'))
            for i, item in enumerate(items):
                if item.get('name') in general_view_list and app.get('name') not in ['General', 'Performance']:
                    general_view.append(item)
            for i, item in enumerate(items):
                if item.get('name') in ['Total_network_outgoing', 'Total_network_incoming', 'Disk_total_read',
                                        'Disk_total_write']:
                    items.remove(items[i])
            app.update(items=items)
        host.update(general_view=general_view)
        host.update(applications=apps)
        graphs = self.get_host_graphs(curtime, period, **host)
        host.update(graphs=graphs)
        return host

    def get_hosts_datas(self, curtime, period, hostids):
        data = []

        host_list = []
        if len(hostids) == 0:
            hosts = self.get_all_hosts()
            for host in hosts:
                host_list.append(host.get('name'))
            info = {
                'host_list': host_list
            }
            return info, self.get_all_data(curtime, period)
        else:
            for hostid in hostids:
                host = self.zabbix_client.get_hosts(hostid)[0]
                host_list.append(host.get('name'))
                data.append(self.get_host_data(hostid, curtime, period))
            info = {
                'host_list': host_list
            }
            return info, data
