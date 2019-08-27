from apps.util.zabbix_client.zabbix_api_source.api_wrapper import ZabbixServerProxy
import time
import re

GRAPH_GROUP = ['network', 'rabbitmq', 'redis', 'memory', 'raid', 'swap', 'mysql', 'disk', 'cpu']


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f %s" % (value, s)
    return "{}B".format(n)


def lastclock_handler(lastlock):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastlock))


def key_handler(item_key_):
    '''
    'key_': 'vfs.fs.size[/,pfree]'
    '''
    pattern = re.compile(r'\[.*\]')
    info = pattern.search(item_key_)
    if info:
        x = info.group()
        c = x.replace(']', '')
        m = c.replace('[', '')
        return m.split(',')


def name_handler(item_name):
    '''

    'Free disk space on $1 (percentage)'

    :param item_name:
    :return: [] ex:['$1', '$2']
    '''
    pattern = re.compile(r'\$\d+')
    info = pattern.findall(item_name)
    return info


def item_name_handler(item_name, item_key_):
    '''
    'vfs.fs.size[/,pfree]'
    'Free disk space on $1  $2(percentage)'
    :param item_name:
    :param item_key_:
    :return: string
    '''
    name = name_handler(item_name)
    item_key = key_handler(item_key_)
    item = ''
    if len(name) != 0:
        for k in name:
            item = item_name.replace(k, item_key[int(k.split('$')[1]) - 1])
    else:
        item = item_name
    return item


def item_value_handler(value, units):
    if units == 'B':
        value = int(value)
        return bytes2human(value)
    elif units == 'uptime' or units == 'unixtime':
        return lastclock_handler(int(value))
    else:
        return str(value) + ' ' + units


def item_value_change(lastvalue, prevvalue, units):
    if units == "B":
        lastvalue = int(lastvalue)
        prevvalue = int(prevvalue)
        if prevvalue == 0:
            return '-'
        else:
            v_change = (1 - (lastvalue/prevvalue)) * 100
            if v_change < 0:
                return str(round(v_change, 2)) + " %"
            else:
                return "+" + str(round(v_change, 2)) + " %"
    elif units == '%':
        lastvalue = float(lastvalue)
        prevvalue = float(prevvalue)
        if prevvalue == 0:
            return '-'
        else:
            v_change = (1 - (lastvalue / prevvalue)) * 100
            if v_change < 0:
                return str(round(v_change, 2)) + " %"
            else:
                return "+" + str(round(v_change, 2)) + " %"
    else:
        return '-'


def item_network_handler_veth(item_name):
    # 'Incoming network traffic on vethcce8b35'
    pattern = re.compile(r'veth')

    item = pattern.findall(item_name)
    if len(item) == 0:
        return False
    else:
        return True


def graph_handler(graph_name):
    # 'Incoming network traffic on vethcce8b35'
    pattern = re.compile(r'veth'
                         r'|WAN Miniport|vif|virbr0|Microsoft'
                         r'|RAS|Zabbix|Value cache'
                         r'|Disk space usage \/var\/lib\/docker\/containers'
                         r'|Disk space usage \/var\/lib\/docker\/overlay2'
                         r'|Disk space usage C:$|Disk space usage D:$|Network traffic on br-cde7d82a0b3c'
                         r'|Network traffic on docker_gwbridge')
    item = pattern.findall(graph_name)
    if len(item) == 0:
        return False
    else:
        return True


def graph_groups(graph_name):
    graph_name = graph_name.lower()
    pattern = re.compile(r'cpu|network|disk|swap|mysql|memory|raid|redis|rabbitmq')
    info = pattern.findall(graph_name)
    return info


def generate_network_interfaces(**item):
    if item.get('name').startswith('Outgoing'):
        pass


class ZabbixClient(object):

    def __init__(self, **kwargs):
        self.zabbix_api = kwargs.get('api')
        self.zabbix_username = kwargs.get('username')
        self.zabbix_password = kwargs.get('password')
        self.conn = self._init()

    def _init(self):
        s = ZabbixServerProxy(self.zabbix_api)
        s.user.login(user=self.zabbix_username, password=self.zabbix_password)
        return s

    def get_base_hosts(self):
        hosts = self.conn.call(method='host.get')
        return hosts

    def get_hosts(self, hostid=None):
        params = {
            'output': ["hostid", "host", "name"],
            'hostids': hostid,
        }
        return self.conn.call(method="host.get", params=params)

    def get_applications(self, hostid, applicationids=None):
        """
        获取zabbix应用集
        :return: list
        """
        params = {
            "output": ["applicationid", "name"],
            "hostids": hostid,
            "applicationids": applicationids,
            "sortfield": "name"
        }

        apps = self.conn.call(method='application.get', params=params)
        new_apps = []
        delete_list = ['Zabbix agent',
                       'Zabbix server',
                       'Zabbix proxy',
                       'Startup automatic delayed services',
                       'Startup automatic services',
                       'Security',
                       'Logstash-zabbix']
        for app in apps:
            if app.get('name') not in delete_list:
                new_apps.append(app)
        return new_apps

    def get_host_monitor_item_values(self, hostid, graphids=None):
        params = {
            "hostids": hostid,
            "graphids": graphids,
            # "output": ["key_", "name", "lastvalue", "type", "prevvalue", "lastclock"],
            "output": ["key_", "name", "lastvalue", "prevvalue", "lastclock", "units", 'error'],
        }
        return self.conn.call(method='item.get', params=params)

    def get_host_monitor_item_values_with_application(self, hostid, application_name=None, applicationid=None, graphids=None):

        params = {
            "hostids": hostid,
            "applicationids": applicationid,
            "graphids": graphids,
            "output": ["key_", "name", "lastvalue", "prevvalue", "lastclock", "units", 'error'],
        }
        new_items = []
        network_incoming_b = []
        network_outgoing_b = []
        disk_wirte_b = []
        disk_read_b = []
        items = self.conn.call(method='item.get', params=params)
        for item in items:
            if item.get('error') == '':
                if item.get('name').startswith('Outgoing network'):
                    network_outgoing_b.append(int(item.get('lastvalue')))
                if item.get("name").startswith('Incoming network'):
                    network_incoming_b.append(int(item.get('lastvalue')))
                if item.get('name').endswith('每秒写数据量'):
                    disk_wirte_b.append(float(item.get('lastvalue')))
                if item.get('name').endswith('每秒读数据量'):
                    disk_read_b.append(float(item.get('lastvalue')))
                change_rate = item_value_change(item.get('lastvalue'), item.get('prevvalue'), item.get('units'))
                item.update(change_rate=change_rate)
                lastcheck_time = lastclock_handler(int(item.get('lastclock')))
                name = item_name_handler(item.get('name'), item.get('key_'))
                item.update(name=name)
                item.pop('key_')
                item.update(lastclock=lastcheck_time)
                lastvalue = item_value_handler(item.get('lastvalue'), item.get('units'))
                item.update(lastvalue=lastvalue)
                prevvalue = item_value_handler(item.get('prevvalue'), item.get('units'))
                item.update(prevvalue=prevvalue)
                item.pop('units')
                item.pop('error')
                if item_network_handler_veth(item.get('name')):
                    continue
                new_items.append(item)
        if application_name == 'Network interfaces':
            Total_network_incoming = {
                'itemid': '99999',
                "name": "Total network incoming per second",
                'lastvalue': bytes2human(sum(network_incoming_b)),
                'change_rate': '-'
            }
            Total_network_outgoing = {
                'itemid': '99998',
                "name": "Total network outgoing per second",
                "lastvalue": bytes2human(sum(network_outgoing_b)),
                'change_rate': '-'
            }
            new_items.append(Total_network_incoming)
            new_items.append(Total_network_outgoing)
        if application_name == 'Disk_IO_Stats':
            Disk_total_read = {
                'itemid': '99997',
                "name": "Disk total read per second",
                'lastvalue': bytes2human(sum(disk_read_b)),
                'change_rate': '-'
            }
            Disk_total_write = {
                'itemid': '99996',
                "name": "Disk total write per second",
                "lastvalue": bytes2human(sum(disk_wirte_b)),
                'change_rate': '-'
            }
            new_items.append(Disk_total_write)
            new_items.append(Disk_total_read)

        return new_items

    def get_host_graphids(self, hostid):
        '''
        :param hostid:
        :return: []
        '''
        params = {
            "hostids": hostid,
            "output": ["graphid", "name", "graphtype"],
            "sortfield": "name"
        }
        ghs = self.conn.call(method='graph.get', params=params)
        new_ghs = []
        for g in ghs:
            if graph_handler(g.get("name")):
                continue
            new_ghs.append(g)
        return new_ghs
