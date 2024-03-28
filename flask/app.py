import requests
import time
import socket
import threading
from bs4 import BeautifulSoup
from lxml import etree
#jinja2渲染模板
from flask import Flask,render_template,request#渲染模板
from datetime import datetime

app=Flask(__name__)
#使用flask创建一个app'对象，__name__代表当前模块

#过滤器
def datetime_format(value,format="%Y-%d-%m %H:%M"):
    return value.strftime(format) 
app.add_template_filter(datetime_format,"dformat")

@app.route("/")#根路由
#创建一个路由和视图函数的映射
def hello_world():
    return render_template("index.html")

@app.route("/SubDomain")
def SubDomain():
    return render_template("SubDomain.html")

#动态参数，类，字典
@app.route("/SubDomainResult",methods=['POST'])
def SubDomainResult():

    domain=request.form.get('url')
    outcome=[]
    page=2

    url = 'http://global.bing.com/search?q=site%3A'+domain+'&qs=n&form=QBRE&sp=-1&pq=site%3A'+domain+'&sc=2-11&sk=&cvid=C1A7FC61462345B1A71F431E60467C43'

    headers = {
        'User-Agent': 'ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400 QQBrowser/9.7.12661.400',
        'Host': 'global.bing.com',
        'Referer': 'http://global.bing.com/?FORM=HPCNEN&setmkt=en-us&setlang=en-us',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'DUP=Q=xa-EfMBM4gI7W690UHSTmQ2&T=312971513&A=2&IG=5161BB1CD80C4B8F8E04213C9A6BB2F1; MUID=35B121D519D96CA802AF2AE41DD96FD2; SRCHD=AF=HPCNEN; SRCHUID=V=2&GUID=59BB79AC0CDE4D8F853C004286CA05C4&dmnchg=1; SRCHUSR=DOB=20171201; MUIDB=35B121D519D96CA802AF2AE41DD96FD2; ULC=H=1D535|1:1&T=1D535|1:1; _RwBf=s=70&o=16; ipv6=hit=1512120707130&t=4; _EDGE_S=mkt=en-us&ui=en-us&SID=0AC562F3333D612722A469B832E160FE; SNRHOP=I=&TS=; _SS=SID=0AC562F3333D612722A469B832E160FE&HV=1512117115&R=0&bIm=473689; SRCHHPGUSR=CW=654&CH=997&DPR=1&UTC=480&WTS=63647713897'
    }
    for i in range(1, int(page)):
        data = {
            'q': 'site:'+domain,
            'qs': 'n',
            'sp': '3',
            'sc': '0-12',
            'sk': '',
            'cvid': '710C7FF1A9B741C29D93EA4CCC435B27',
            'first': i*12,
            'FORM': 'PERE'
        }
        sessions = requests.Session()
        results = sessions.get(url, headers=headers, params=data,allow_redirects=False)
        soup = BeautifulSoup(results.content, 'html.parser')
        job_bt = soup.findAll('h2')
        for i in job_bt:
            outcome.append(i.a.get('href'))
        time.sleep(1)

    return render_template("SubDomainResult.html",result1=outcome,url=domain)

@app.route("/Whois")
def Whois():
    return render_template("whois.html")

@app.route("/WhoisResult", methods=['POST'])
def WhoisResult():
    domain=request.form.get('url')
    results1=""
    results2=""
    results3=""

    url = "https://whois.chinaz.com/" + domain
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    messages1 = tree.xpath('//div[@id="whois_info"]//li[@class="clearfix bor-b1s"]')
    messages2 = tree.xpath('//div[@id="whois_info"]//li[@class="clearfix bor-b1s "]')
    messages3 = tree.xpath('//div[@id="whois_info"]//li[@class="clearfix bor-b1s  "]')

#with open("WhoisReport.txt", "w+", encoding="utf-8") as fp:
    #fp.write(f"域名：{domain}\n")
    for message in messages1:
        left_info = ''.join(message.xpath('.//div[@class="fl WhLeList-left"]//text()')).strip()
        right_info1 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right"]//span//text()')).strip()
        right_info2 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right clearfix"]//span//text()')).strip()
        result1=f"{left_info}: {right_info1} {right_info2}\n"
        results1=f"{results1}\n{result1}\n"
    for message in messages2:
        left_info = ''.join(message.xpath('.//div[@class="fl WhLeList-left"]//text()')).strip()
        right_info1 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right"]//span//text()')).strip()
        right_info2 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right clearfix"]//span//text()')).strip()
        result2=f"{left_info}: {right_info1} {right_info2}\n"
        results2=f"{results2}\n{result2}\n"
    for message in messages3:
        left_info = ''.join(message.xpath('.//div[@class="fl WhLeList-left"]//text()')).strip()
        right_info1 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right"]//span//text()')).strip()
        right_info2 = ', '.join(message.xpath('.//div[@class="fr WhLeList-right clearfix"]//span//text()')).strip()
        result3=f"{left_info}: {right_info1} {right_info2}\n"
        results3=f"{results3}\n{result3}\n"

    if results1=="" and results2=="" and results3=="":
        results1="您输入的url有误 请输入正确url"

    return render_template("WhoisResult.html",result1=results1,result2=results2,result3=results3,url=domain)

@app.route("/PortscanSearch")
def PortscanSearch():
    return render_template("PortscanSearch.html")

@app.route("/Portscan",methods=['POST'])
def Portscan():

    ip = request.form.get('url')
    open_ports = []
    thread_lock = threading.Lock()

    def scan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        with thread_lock:
            try:
                s.connect((ip, port))
                open_ports.append(port)
                print("["+str(port)+"]" + " is open")
            except:
                pass
            finally:
                s.close()

    first_port = int(request.form.get('fport'))
    last_port = int(request.form.get('lport'))

    start_time = time.time()
    threads = []

    for i in range(first_port, last_port+1):
        t = threading.Thread(target=scan, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    #print("\n扫描端口个数:")
    #print(last_port - first_port + 1)
    #print("\n开放的端口:")
    #print(open_ports)
    counttime="%.2f seconds" % (time.time() - start_time)
    if open_ports==[]:
        open_ports="没有开放端口"
        
    open_ports1=str(open_ports)

    return render_template("Portscan.html",port=open_ports1,ip=ip,counttime=counttime)

if __name__ =="__main__":
    app.run(debug=True,host="0.0.0.0",port=9000)
