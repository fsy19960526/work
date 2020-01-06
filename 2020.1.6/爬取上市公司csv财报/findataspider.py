
import requests
from lxml import etree
from time import sleep


class Spider():
    def __init__(self):


        #三表在URL中的名称，基本URL
        self.data_name=['zcfzb','lrb','xjllb']
        self.service_url='http://quotes.money.163.com/service/{}_{}.html'


        #各个报表的URL
        self.service_url_equity='http://quotes.money.163.com/service/zcfzb_{}.html'
        self.service_url_profits='http://quotes.money.163.com/service/lrb_{}.html'
        self.service_url_cashflow='http://quotes.money.163.com/service/xjllb_{}.html'


        #股票列表的URL
        self.url='http://quotes.money.163.com/data/caibao/yjgl_ALL.html?reportdate=20190930&sort=publishdate&order=desc&page=0'
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                      'Cookie':"_ntes_nnid=5fa9d2531baf7d9a16fe283f04d64ca8,1562564856414; _ntes_nuid=5fa9d2531baf7d9a16fe283f04d64ca8; mail_psc_fingerprint=030749b0b12aa8984cf3ea5ebf508a8e; P_INFO=fsy19960526@163.com|1571119436|0|youdaonote|00&99|null&null&null#bej&null#10#0|&0||fsy19960526@163.com; vjuids=-62cab8b59.16f78a22229.0.a0f48bcf69fb4; vjlast=1578276889.1578276889.30; ne_analysis_trace_id=1578276889239; s_n_f_l_n3=08d02e651018fbcf1578276889244; vinfo_n_f_l_n3=08d02e651018fbcf.1.1.1574944605336.1574944649904.1578277161971",
                      "Host": "quotes.money.163.com"}

    #获取decode()返回值
    def get_url(self,url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    #获取所有页面的url
    def get_url_list(self,url):
        html_str=self.get_url(url)
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@class='mod_pages']/a/@href")
        div_ret_list=[int(div.split('=')[4]) for div in div_list]
        max_num=max(div_ret_list)
        div_url_list=['http://quotes.money.163.com/data/caibao/yjgl_ALL.html?reportdate=20190930&sort=publishdate&order=desc&page={}'.format(i) for i in range(0,max_num+1)]
        return div_url_list

    #获取财务报表的url地址，并存储
    def url_request(self,div_url_list):
        global stock_profits, stock_equity, stock_cashflow, stock
        stock_list=[]
        for url in div_url_list:
            response = requests.get(url, headers=self.headers)
            html_str=response.content.decode()
            html = etree.HTML(html_str)
            div_list = html.xpath( "// table[ @class ='fn_cm_table'] //td/a/text()")
            stock=[div for div in div_list if div.isdigit()]
            stock_list=stock_list+stock
            stock_equity=[self.service_url_equity.format(stock) for stock in stock_list]
            stock_profits = [self.service_url_profits.format(stock) for stock in stock_list]
            stock_cashflow= [self.service_url_cashflow.format(stock) for stock in stock_list]
            print(stock)

        with open('stock_list.txt',"a", encoding='utf-8') as f:
            for stname in stock_list:
                f.write(stname)
                f.write('\n')
        return stock_list

    #读取存有股票代码的txt
    def read_url_list(self):

        with open('stock_list.txt','r') as f:
            stname=f.read()
            stock=stname.split('\n')

        return stock
    #保存为csv格式的三表文件
    def read_save(self,stock):

        for stname in stock:
            response1 = requests.get(self.service_url.format(self.data_name[0],stname), headers=self.headers)
            with open('{}_equity.csv'.format(stname), 'wb') as f:
                     f.write(response1.content)
            response2 = requests.get(self.service_url.format(self.data_name[1], stname), headers=self.headers)
            with open('{}_profits.csv'.format(stname), 'wb') as f:
                     f.write(response2.content)
            response3= requests.get(self.service_url.format(self.data_name[2], stname), headers=self.headers)
            with open('{}_cashflow.csv'.format(stname), 'wb') as f:
                     f.write(response3.content)
            print('{}三表保存完成'.format(stname))
            sleep(0.5)
    def run(self):
        #1.提取url，构建url_list
        # div_url_list=self.get_url_list(self.url)
        # stock=self.url_request(div_url_list)
        #1.1在读取完成后，之后可以通过txt文档读取url_list
        # stock,stock_equity,stock_profits,stock_cashflow=self.read_url_list()
        stock= self.read_url_list()
        #2.发送请求
        self.read_save(stock)
        #3.提取数据
        #4.保存
        pass
if __name__ == '__main__':
    spider=Spider()
    spider.run()
