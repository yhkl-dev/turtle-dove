# from zabbix_api_source.handler import ZabbixDataHandler
from apps.util.zabbix_client.zabbix_api_source.handler import ZabbixDataHandler
from django.conf import settings
from PyPDF2 import PdfFileMerger
import datetime
import jinja2
import os
import subprocess

TEMPLATE_FILE_PATH = settings.BASE_DIR + '/templates/'

WKHTMLTOPDF = 'xvfb-run -a --server-args="-screen 0, ' \
              '1024x768x24" /usr/bin/wkhtmltopdf --page-size A4 --margin-top 0.5in ' \
              '--margin-right 0.75in --margin-bottom 0.75in --margin-left 0.5in --encoding utf-8 --quiet'

ctime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
HTML_FILE_PATH = '/tmp/html_files/'
PDF_FILE_PATH = '/tmp/pdf_files/'
MERGE_PDF_FILE_PATH = '/tmp/check_report/'

if not os.path.isdir(HTML_FILE_PATH):
    os.makedirs(HTML_FILE_PATH)

if not os.path.isdir(PDF_FILE_PATH):
    os.makedirs(PDF_FILE_PATH)

if not os.path.isdir(MERGE_PDF_FILE_PATH):
    os.makedirs(MERGE_PDF_FILE_PATH)


def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(**kwargs)


def is_exist(file_name):
    if os.path.exists(file_name):
        return True
    else:
        return False


def generate_html(server_info, html_file_path):
    hostname = server_info.get('host')
    content = render(TEMPLATE_FILE_PATH + 'template_1.html', **server_info)
    file_name = html_file_path + '{}-{}.html'.format(hostname, ctime)
    if not is_exist(file_name):
        with open(file_name, 'w') as f:
            f.write(content)
        f.close()
    return file_name


def generate_pdf(html_file_name, pdf_file_path):
    file_name = html_file_name.split('.')[0]
    pdf_file_name = '{}.pdf'.format(os.path.basename(file_name))

    try:
        subprocess.getoutput('{} {} {} '.format(WKHTMLTOPDF, html_file_name, pdf_file_path+pdf_file_name))
        # print("GENERATE PDF SUCCESS")
        return pdf_file_path+pdf_file_name
    except Exception as e:
        print(e)


def merge_pdf(pdfs, merge_pdf_file_path):
    merger = PdfFileMerger()
    for pdf_name in pdfs:
        # print(pdf_name)
        merger.append(open(pdf_name, 'rb'))
    cstime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_file_name = '{}{}.pdf'.format(merge_pdf_file_path, 'server-report-{}%'.format(cstime))
    with open(report_file_name, 'wb') as fout:
        merger.write(fout)
    print('MERGE PDF FILE OK!')
    return report_file_name


def clean_file(html_file_path, pdf_file_path):
    """ 清理临时文件 """
    print('CLEAN TEMPLATE FILES..')
    for root, dirs, files in os.walk(html_file_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

    for root, dirs, files in os.walk(pdf_file_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

    print('CLEAN TEMPLATE FILES DONE..')


def generate_index(host_list, html_file_path, pdf_file_path):
    html_file_name = html_file_path + 'report_index.html'
    content = render(TEMPLATE_FILE_PATH + 'template_2.html', **host_list)
    with open(html_file_name, 'w') as f:
        f.write(content)
    f.close()
    return generate_pdf(html_file_name, pdf_file_path)


def add_homepage(merge_pdf_file_name):
    file_name = merge_pdf_file_name.split('%')[0] + '.pdf'
    merger_pdf = PdfFileMerger()
    input = open(merge_pdf_file_name, 'rb')
    input1 = open(TEMPLATE_FILE_PATH + 'homepage.pdf', 'rb')
    merger_pdf.append(input1)
    merger_pdf.append(input)
    with open(file_name, 'wb') as f:
        merger_pdf.write(f)
    os.remove(merge_pdf_file_name)
    return file_name


def add_index(merge_pdf_file_name, index_page_file_name):
    file_name = merge_pdf_file_name.split('.')[0] + '_with_index.pdf'
    merger_pdf = PdfFileMerger()
    input = open(merge_pdf_file_name, 'rb')
    input1 = open(index_page_file_name, 'rb')
    merger_pdf.append(input1)
    merger_pdf.append(input)
    with open(file_name, 'wb') as f:
        merger_pdf.write(f)
    os.remove(merge_pdf_file_name)
    return file_name


def generate_report_files(html_file_path, pdf_file_path, merge_pdf_file_path, curtime, period,  hostid_list, **zabbix_info):
    '''

    :param hostid_list: 主机列表
    :param html_file_path:  html临时文件路径
    :param pdf_file_path:  pdf临时文件路径
    :param merge_pdf_file_path:  巡检报告路径
    :param curtime: 指定时间 格式为时间戳，
    :param period: 巡检时间间隔 如：巡检当前时间至1小时之前 curtime 为当前时间，period 单位为秒 3600s
    :param zabbix_info: zabbix 服务器信息
    :return: 巡检报告文件路径
    '''
    clean_file(html_file_path, pdf_file_path)
    service = ZabbixDataHandler(**zabbix_info)
    host_list, datas = service.get_hosts_datas(curtime, period, hostid_list)
    pdfs = []
    index_file_name = generate_index(host_list, html_file_path, pdf_file_path)
    for data in datas:
        html_file_name = generate_html(data, html_file_path)
        pdf_file_name = generate_pdf(html_file_name, pdf_file_path)
        pdfs.append(pdf_file_name)
    orgin_file = merge_pdf(pdfs, merge_pdf_file_path)
    report_file_name = add_index(orgin_file, index_file_name)
    fina_file = add_homepage(report_file_name)
    clean_file(html_file_path, pdf_file_path)
    return fina_file


if __name__ == '__main__':
    zabbix_info = {
        "api": "http://192.168.1.54/zabbix",
        "username": 'admin',
        "password": 'zabbix',
        "login_url": 'http://192.168.1.54/zabbix/index.php',
        "graph_url": 'http://192.168.1.54/zabbix/chart2.php',
        "pie_graph_url": 'http://192.168.1.54/zabbix/chart6.php'
    }
    curtime = round(datetime.datetime.now().timestamp() * 1000)
    period = 3600
    host_list = []
    pdf_file_name = generate_report_files(HTML_FILE_PATH,
                                          PDF_FILE_PATH,
                                          MERGE_PDF_FILE_PATH,
                                          curtime,
                                          period,
                                          host_list,
                                          **zabbix_info)
    print(pdf_file_name)
