import requests


class ZabbixGraph(object):
    '''
        获取zabbix生成的图片
    '''

    def __init__(self, username, password, login_url):
        self.username = username
        self.password = password
        self.login_url = login_url
        self.sessions = self._login(login_url, username, password)

    def _login(self, login_url, username, password):
        '''
        func login

        :param login_url: 登录zabbix serverurl http://zabbix-server/zabbix/index.php
        :param username: ..
        :param password: ..
        :return: session 用于操作zabbix 获取相关数据
        '''
        s = requests.session()
        login_url = '{}?name={}&password={}&autologin=1&enter=Sign+in'.format(self.login_url, self.username, self.password)
        s.get(login_url)
        s.headers = {
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "zbx_sessionid={}".format(s.cookies["zbx_sessionid"]),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; \
            Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        return s

    def get_graph_chart2(self, image_path, graph_url, hostid, hostname, graph_name, graphid, curtime, period,
                         width):
        '''
        生成 picture
        url 样例：
            http://192.168.1.54/zabbix/chart2.php?
                graphid=847&
                period=86400
                &stime=20190602150409
                &isNow=0
                &profileIdx=web.graphs
                &profileIdx2=847
                &width=1782
                &sid=c0cedd0a8b82a9f4
                &screenid=
                &curtime=1559697192440

        :param image_path: 图片保存路径
        :param graph_url: 饼图url
        :param hostid:  主机id
        :param hostname:  主机name
        :param graph_name: 图片名称
        :param graphid: 图片id
        :param curtime: 当前时间
        :param stime: 数据开始时间，用于url采集
        :param period: 数据周期，如: 1小时 3600s， 一天：86400s 注意 单位是秒
        :return: 生成的图片路径
        '''
        hostnames = hostname.replace(' ', '-')
        a = graph_name.lower()
        b = a.replace(' ', '-')
        c = b.replace('/', 'DIR-')
        url = '{0}?hostid={1}&graphid={2}&period={3}&width={4}&curtime={5}'.format(
            graph_url, hostid, graphid, period, width, curtime
        )
        data = self.sessions.get(url)
        png_name = image_path + "{}-{}.png".format(hostnames, c)
        with open(png_name, 'wb') as f:
            f.write(data.content)

        return png_name

    def get_graph_chart6(self, image_path, graph_url, hostid, hostname, graph_name, graphid, curtime, period):
        '''
        Pie picture
        url 样例：
            http://192.168.1.54/zabbix/chart2.php?
                graphid=847&
                period=86400
                &stime=20190602150409
                &isNow=0
                &profileIdx=web.graphs
                &profileIdx2=847
                &width=1782
                &sid=c0cedd0a8b82a9f4
                &screenid=
                &curtime=1559697192440

        :param image_path: 图片保存路径
        :param graph_url: 饼图url
        :param hostid:  主机id
        :param hostname:  主机name
        :param graph_name: 图片名称
        :param graphid: 图片id
        :param curtime: 当前时间
        :param stime: 数据开始时间，用于url采集
        :param period: 数据周期，如: 1小时 3600s， 一天：86400s 注意 单位是秒
        :return: 生成的图片路径
        '''
        hostnames = hostname.replace(' ', '-')
        a = graph_name.lower()
        b = a.replace(' ', '-')
        c = b.replace('/', 'DIR-')
        d = c.replace(':\\', '')

        # url = '{0}?hostid={1}&graphid={2}&period={3}&stime={4}&curtime={5}'.format(
        #     graph_url, hostid, graphid, period, stime, curtime
        # )
        url = '{0}?hostid={1}&graphid={2}&period={3}&curtime={4}'.format(
            graph_url, hostid, graphid, period, curtime
        )
        data = self.sessions.get(url)
        png_name = image_path + "{}-{}.png".format(hostnames, d)
        with open(png_name, 'wb') as f:
            f.write(data.content)
        return png_name
