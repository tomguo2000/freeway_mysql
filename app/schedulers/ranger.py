import base64
import datetime
# from app.utils.setLogger import logger
import os
import socket
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
import ssl
from retrying import retry
import smtplib
from email.mime.text import MIMEText
import json


def convert2HTML(report):
    if not isinstance(report, dict):
        report = json.loads(report)

    # 解析JSON数据
    data = report

    # 获取当前的日期和时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 开始构建HTML文档
    html_report = f"""  
    <!DOCTYPE html>  
    <html lang="en">  
    <head>  
        <meta charset="UTF-8">  
        <title>Ranger Report</title>  
        <style>  
            body {{ font-family: Arial, sans-serif; }}  
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}  
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}  
            th {{ background-color: #f2f2f2; }}  
            .ok {{ background-color: #d4edda; }}  
            .error {{ background-color: #f8d7da; }}  
        </style>  
    </head>  
    <body>  
        <h1>Ranger Report on: {current_time}</h1>  
    """

    # 循环遍历数据，为每个部分生成一个HTML表格
    for section, entries in data.items():
        html_report += f"<h2>{section}</h2>\n"
        html_report += "<table>\n"

        # 表头
        if entries:
            html_report += "<tr>\n"
            for header in entries[0].keys():
                html_report += f"<th>{header}</th>\n"
            html_report += "</tr>\n"

        # 表数据
        for entry in entries:
            # 根据result字段的值设置行的类
            row_class = "ok" if entry.get("result") == "ok" else "error"
            html_report += f'<tr class="{row_class}">\n'
            for key, value in entry.items():
                html_report += f"<td>{value}</td>\n"
            html_report += "</tr>\n"
        html_report += "</table>\n"

    # 结束HTML文档
    html_report += """
    </body>
    </html>
    """

    # 打印HTML报告
    return html_report

    # # 或者将HTML报告写入到一个文件中
    # with open('connectivity_report.html', 'w', encoding='utf-8') as file:
    #     file.write(html_report)


def mailout(text):
    host = 'smtp.163.com'
    # 设置发件服务器地址
    port = 465
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
    sender = 'thunderglobal@163.com'
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = os.getenv("MAIL_PWD")
    # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    receiver = os.getenv("MAILTO")
    # 设置邮件接收人，可以是QQ邮箱
    body = text
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html')
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = "Thunder Ranger"
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    msg['to'] = receiver
    # 设置接收人

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())

        print(f"send report success on {current_time}")
        return 200
    except Exception as ex:
        print(ex,current_time)
        return 404


class DownloadURL:
    def __init__(self, url):
        self.url = url

        parsed_url = urlparse(url)
        self._scheme = parsed_url.scheme
        self._domain = parsed_url.hostname
        if self._scheme == 'https':
            self._port = parsed_url.port if parsed_url.port else 443
        else:
            self._port = parsed_url.port if parsed_url.port else 80

        self.can_download = None
        self.cert_expire_date = None


class PaymentGW:
    def __init__(self, url):
        self.url = url

        parsed_url = urlparse(url)
        self._scheme = parsed_url.scheme
        self._domain = parsed_url.hostname
        if self._scheme == 'https':
            self._port = parsed_url.port if parsed_url.port else 443
        else:
            self._port = parsed_url.port if parsed_url.port else 80

        self.is_domain_connectable = None
        self.cert_expire_date = None


class DomainList:
    def __init__(self, url):
        self.url = url

        parsed_url = urlparse(url)
        self._scheme = parsed_url.scheme
        self._domain = parsed_url.hostname
        if self._scheme == 'https':
            self._port = parsed_url.port if parsed_url.port else 443
        else:
            self._port = parsed_url.port if parsed_url.port else 80

        self.is_domain_connectable = None
        self.cert_expire_date = None




class TrojanNode:
    def __init__(self, url):
        self.url = url

        parsed_url = urlparse(url)
        self._scheme = parsed_url.scheme
        self._domain = parsed_url.hostname
        if self._scheme == 'https':
            self._port = parsed_url.port if parsed_url.port else 443
        else:
            self._port = parsed_url.port if parsed_url.port else 80

        self.is_domain_connectable = None
        self.cert_expire_date = None



class PortalNode:
    def __init__(self, portalVersion, url):
        self.portalVersion = portalVersion
        self.url = url

        parsed_url = urlparse(url)
        self._scheme = parsed_url.scheme
        self._domain = parsed_url.hostname
        if self._scheme == 'https':
            self._port = parsed_url.port if parsed_url.port else 443
        else:
            self._port = parsed_url.port if parsed_url.port else 80

        self.is_domain_connectable = None
        self.cert_expire_date = None
        self.is_response_correct = None



class Ranger:

    def __init__(self):
        self.status = None


    def loadConfig(self):
        self.status = 'preparing'

        dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path, override=True)

        # config CertExpAlertDays
        self.certExpAlertDays = int(os.getenv("CERT_EXP_ALERT"))

        # config Portal
        v3PortalUrl = os.getenv("ANDROID_V3")
        v6PortalUrl = os.getenv("PORTAL_V6")

        v3data = requests.get(v3PortalUrl, timeout=5).text
        v3data = base64.decodebytes(v3data.encode()).decode()

        v3dataList=v3data.split('<->')
        v3Portal = []
        for portalUrl in v3dataList:
            _portalNode = PortalNode('v3', self.findContent(portalUrl, head='url=', end='|'))
            v3Portal.append(_portalNode)

        self.v3Portal = v3Portal

        v6data = requests.get(v6PortalUrl, timeout=5).text
        v6data = self.parseV6Data(v6data)

        v6Portal = []
        for portalUrl in v6data['api_gateway']:
            _portalNode = PortalNode('v6', portalUrl)
            v6Portal.append(_portalNode)
        self.v6Portal = v6Portal


        # config trojan nodes
        trojan_nodes = os.getenv("TROJAN_NODES")

        self.trojan_nodes = []
        for item in trojan_nodes.split(","):
            self.trojan_nodes.append(TrojanNode(item.strip()))


        # config domain list
        domain_list = os.getenv("DOMAIN_LIST")
        self.domain_list = []
        for item in domain_list.split(","):
            self.domain_list.append(DomainList(item.strip()))


        # config paymentGWs
        payment_gw_pony = os.getenv("PAYMENT_GW_PONY")
        payment_gw_expresspay = os.getenv("PAYMENT_GW_EXPRESSPAY")
        payment_gw_android = os.getenv("PAYMENT_GW_ANDROID")
        payment_gw = os.getenv("PAYMENT_GW")

        self.payment_gw_list = []
        for item in payment_gw_pony.split(","):
            self.payment_gw_list.append(PaymentGW(item.strip()))
        for item in payment_gw_expresspay.split(","):
            self.payment_gw_list.append(PaymentGW(item.strip()))
        for item in payment_gw_android.split(","):
            self.payment_gw_list.append(PaymentGW(item.strip()))
        for item in payment_gw.split(","):
            self.payment_gw_list.append(PaymentGW(item.strip()))


        # config download url
        download_urls = os.getenv("DOWNLOAD_URL")
        self.download_urls = []
        for item in download_urls.split(","):
            self.download_urls.append(DownloadURL(item.strip()))

    def checkDownloadURL(self):
        for item in self.download_urls:
            # check download able
            try:
                # 发送HEAD请求
                response = requests.head(item.url, allow_redirects=True)
                # 检查状态码
                if response.status_code == 200:
                    # 检查Content-Type是否存在
                    content_type = response.headers.get('Content-Type')
                    # 检查Content-Length是否存在
                    content_length = response.headers.get('Content-Length')

                    # 如果Content-Type和Content-Length存在且长度不为0，则认为文件可下载
                    if content_type and (content_length is None or int(content_length) > 0):
                        item.can_download = True

            except requests.RequestException as e:
                print(f"请求发生错误: {e}")
                item.can_download = False

            # check certification expire date
            if item._scheme == 'https':
                item.cert_expire_date = self.checkCertExpDate(item._domain, item._port)
            else:
                item.cert_expire_date = 'N/A'



    def checkPaymentGW(self):
        for node in self.payment_gw_list:
            print(f"start checkPaymentGW on {node.url}")
            # check is_domain_connectable
            node.is_domain_connectable = self.checkDomainConnectable(node._domain, node._port)

            # check certification expire date
            if node._scheme == 'https':
                node.cert_expire_date = self.checkCertExpDate(node._domain, node._port)
            else:
                node.cert_expire_date = 'N/A'



    def checkDomainList(self):
        for node in self.domain_list:
            print(f"start checkDomainList on {node.url}")
            # check is_domain_connectable
            node.is_domain_connectable = self.checkDomainConnectable(node._domain, node._port)

            # check certification expire date
            if node._scheme == 'https':
                node.cert_expire_date = self.checkCertExpDate(node._domain, node._port)
            else:
                node.cert_expire_date = 'N/A'


    def checkTrojanNode(self):
        for node in self.trojan_nodes:

            print(f"start checkTrojanNode on {node.url}")
            # check is_domain_connectable
            node.is_domain_connectable = self.checkDomainConnectable(node._domain, node._port)

            # check certification expire date
            if node._scheme == 'https':
                node.cert_expire_date = self.checkCertExpDate(node._domain, node._port)
            else:
                node.cert_expire_date = 'N/A'


    def parseV6Data(self,dataStr):
        try:
            new_list = []
            point = 0
            while len(dataStr) - point > 8:  # not include last segment
                temp = list(dataStr[point:point + 8])
                temp.reverse()
                new_list.append(''.join(temp))
                point += 8
                point += 2  # skip 2 Noise code
            new_list.append(dataStr[point:])
            decodedStr = ''.join(new_list)
            base64DecodedBytes = base64.b64decode(decodedStr)
            # or return DICT
            base64DecodedDict = json.loads(base64DecodedBytes)

            return base64DecodedDict

        except Exception as ex:
            print(ex)
            return False

    def checkPortal(self):
        self.status = 'running'
        print(f"current function: {sys._getframe().f_code.co_name}")


        for v3Portal in self.v3Portal:
            self._checkPortal(v3Portal)

        for v6Portal in self.v6Portal:
            self._checkPortal(v6Portal)

        print('done')

    @retry(stop_max_attempt_number=3)
    def _checkPortal(self, portalNode):
        print(f"start _checkPortal on {portalNode.url}")
        # check is_domain_connectable
        portalNode.is_domain_connectable = self.checkDomainConnectable(portalNode._domain, portalNode._port)

        # check certification expire date
        if portalNode._scheme == 'https':
            portalNode.cert_expire_date = self.checkCertExpDate(portalNode._domain, portalNode._port)
        else:
            portalNode.cert_expire_date = 'N/A'

        # check response
        try:
            if portalNode.portalVersion == 'v3':
                url = portalNode.url + '/wxapi/xt.php'
                _dataStr = requests.get(url).text
                _json = json.loads(base64.decodebytes(_dataStr.encode()))
                if _json.get('result'):
                    portalNode.is_response_correct = True
                else:
                    portalNode.is_response_correct = False

            elif portalNode.portalVersion == 'v6':
                url = portalNode.url + '/login'
                _dataStr = requests.post(url, timeout=2).text
                _json = json.loads(_dataStr.encode())
                if _json.get('status') == 400:
                    portalNode.is_response_correct = True
                else:
                    portalNode.is_response_correct = False
            else:
                pass
        except Exception as ex:
            portalNode.is_response_correct = False



    def checkDomainConnectable(self, domain, port, timeout=5):
        try:
            # 尝试连接到指定域名和端口
            with socket.create_connection((domain, port), timeout):
                print(f"checkDomainConnectable: Domain {domain} is connectable on port {port}.")
                return True
        except OSError as e:
            print(f"checkDomainConnectable: Domain {domain} is not connectable on port {port}. Error: {e}")
            return False

    def findContent(self,data,head,end):
        try:
            temp = data.split(head)
            return temp[1].split(end)[0]
        except:
            return None


    def checkCertExpDate(self, domain, port):

        print(f"checkCertExpDays: hostname: {domain} port: {port}")
        ssl_context = ssl.create_default_context()
        conn = ssl_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(3.0)
        try:
            conn.connect((domain, port))
            ssl_info = conn.getpeercert()
            expire_date = ssl_info['notAfter']
            expire_date = datetime.datetime.strptime(expire_date, '%b %d %H:%M:%S %Y %Z')
            return str(expire_date)
        except Exception as ex:
            print(f"Error: {ex}")
            return 'ERROR'
        finally:
            conn.close()

    def checkCertExp(self, expDateStr):

        if expDateStr == 'N/A':
            return True

        if expDateStr == 'ERROR':
            return False

        delta = datetime.datetime.strptime(expDateStr, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
        if delta.days > self.certExpAlertDays:
            return True
        else:
            return False


    def run(self):
        self.status = 'start'
        self.loadConfig()
        self.checkPortal()
        self.checkTrojanNode()
        self.checkDomainList()
        self.checkPaymentGW()
        self.checkDownloadURL()


    def genReport(self):

        self.report = {}

        v3Portal = []
        for node in self.v3Portal:
            c = {}
            c['url'] = node.url
            c['is_domain_connectable'] = node.is_domain_connectable
            c['cert_expire_date'] = node.cert_expire_date
            c['is_response_correct'] = node.is_response_correct
            if c['is_domain_connectable'] and c['is_response_correct'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            v3Portal.append(c)
        self.report['v3Portal'] = v3Portal

        v6Portal = []
        for node in self.v6Portal:
            c = {}
            c['url'] = node.url
            c['is_domain_connectable'] = node.is_domain_connectable
            c['cert_expire_date'] = node.cert_expire_date
            c['is_response_correct'] = node.is_response_correct
            if c['is_domain_connectable'] and c['is_response_correct'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            v6Portal.append(c)
        self.report['v6Portal'] = v6Portal

        trojan_nodes = []
        for node in self.trojan_nodes:
            c = {}
            c['url'] = node.url
            c['is_domain_connectable'] = node.is_domain_connectable
            c['cert_expire_date'] = node.cert_expire_date
            if c['is_domain_connectable'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            trojan_nodes.append(c)
        self.report['trojan_nodes'] = trojan_nodes

        domain_list = []
        for node in self.domain_list:
            c = {}
            c['url'] = node.url
            c['is_domain_connectable'] = node.is_domain_connectable
            c['cert_expire_date'] = node.cert_expire_date
            if c['is_domain_connectable'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            domain_list.append(c)
        self.report['domain_list'] = domain_list

        payment_gw_list = []
        for node in self.payment_gw_list:
            c = {}
            c['url'] = node.url
            c['is_domain_connectable'] = node.is_domain_connectable
            c['cert_expire_date'] = node.cert_expire_date
            if c['is_domain_connectable'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            payment_gw_list.append(c)
        self.report['payment_gw_list'] = payment_gw_list


        download_urls = []
        for node in self.download_urls:
            c = {}
            c['url'] = node.url
            c['can_download'] = node.can_download
            c['cert_expire_date'] = node.cert_expire_date
            if c['can_download'] and self.checkCertExp(c['cert_expire_date']):
                c['result'] = 'ok'
            else:
                c['result'] = 'ERROR'
            download_urls.append(c)
        self.report['download_urls'] = download_urls


        self.status = 'finish'


if __name__ == '__main__':
    ranger=Ranger()
    ranger.run()
    ranger.genReport()
    html = convert2HTML(ranger.report)
    mailout(html)

