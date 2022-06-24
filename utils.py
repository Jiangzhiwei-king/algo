# coding:utf8
from multiprocessing import Pool
from selenium import webdriver
import time
import threading
import requests
from proxy import getProxy
# 计时
a = time.time()

class JdSpider(object):
    def __init__(self):
        self.url = ''
        self.options = webdriver.EdgeOptions()  # 无头模式
        self.options.add_argument('--headless')
        self.options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
        self.options.add_argument('window-size=1920x1080')
        self.browser = webdriver.Edge(options=self.options)  
        self.i = 0 
        self.list = []
        self.username = '18269720231'
        self.password = 'Jiangzhiwei123'
        self.count = {'right':0, 'wrong':0,'start':time.time()}
    def get_html(self):
        self.browser.get(self.url)

    def get_data(self):
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        itemlist = self.browser.find_elements_by_xpath(
            '//*[@id="app"]/div/div[5]/div/div/div[2]/div/div[2]/div[2]/div[4]/div/div')
        for item in enumerate(itemlist):
            itemss = {}
            itemss['src'] = item[1].find_elements_by_xpath(
                "./div[1]/a")[0].get_attribute('href')
            self.list.append(itemss)
        print(self.list)

    def get_data_detail(self):
        for data in self.list:
            try:
                itemss = {}
                # 设置代理
                print(getProxy())
                proxies = {'proxy': getProxy()['proxy']}
                # 设置请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                }
                # self.options.add_argument('--proxy-server=http://' + proxies)

                self.browser.get(data['src'],proxies=proxies)
                itemlist = self.browser.find_elements_by_xpath(
                    '//*[@id="app"]/div/div[6]/div/div/div[1]/div[1]/div[2]/div/div')
                tempImageContainer = []
                for item in itemlist:
                    tempImageContainer.append(item.find_elements_by_xpath(
                        './div/img')[0].get_attribute('src').replace('88x88', '960x960'))
                itemss['main_pic'] = tempImageContainer
                try:
                    detail = self.browser.find_elements_by_xpath(
                        '//*[@id="app"]/div/div[6]/div/div/div[1]/div[2]/div')
                except:
                    print('没有大概范围')
                try:
                    itemss['zwd_id'] = data['src'].split('=')[1].split('&')[0]
                except:
                    print('没有zwd_id')
                    itemss['zwd_id'] = ''
                try:
                    itemss['title'] = detail[0].find_elements_by_xpath(
                        './span')[0].text
                except:
                    print('没有title')
                    itemss['title'] = ''
                try:
                    itemss['tb_url'] = detail[0].find_elements_by_xpath(
                        './a')[0].get_attribute('href')
                except:
                    print('没有tb_url')
                    itemss['tb_url'] = ''
                try:
                    itemss['tb_id'] = itemss['tb_url'].split('=')[1]
                except:
                    print('没有tb_id或者没有tb_url,请检查url形式')
                    itemss['tb_id'] = ''
                try:
                    itemss['tb_price'] = detail[1].find_elements_by_xpath(
                        './div[2]/div[1]/div/span[2]')[0].text
                except:
                    print('没有淘宝价格')
                    itemss['tb_price'] = ''
                try:
                    itemss['price'] = detail[1].find_elements_by_xpath(
                        './div[2]/div[2]/div/span[2]')[0].text
                except:
                    print('没有价格')
                    itemss['price']
                try:
                    itemss['item_no'] = detail[2].find_element_by_xpath(
                        './div[1]/div[2]').text
                except:
                    print('没有货号')
                    itemss['item_no'] = ''
                try:
                    itemss['list_time'] = detail[2].find_element_by_xpath(
                        './div[2]/div[2]').text
                except:
                    # 没有添加时间
                    print('没有添加时间')
                    itemss['list_time'] = ''
                try:
                    tt = self.browser.find_elements_by_xpath(
                        '//*[@id="app"]/div/div[6]/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div')
                    tempss = []
                    for item in tt:
                        tempss.append(item.text)
                    itemss['detail'] = tempss
                except:
                    print('没有detail')
                try:
                    print(1110)
                except:
                    print('颜色标签不是图片')
                print(itemss)
                self.count['right'] += 1
                if self.count['right']  == 1:
                    self.count['interval'] = time.time() - self.count['start']
                else:
                    self.count['interval'] = time.time() - self.count['last_time']
                self.count['last_time']= time.time()
                print(self.count)
            except:
                print('出错了', data['src'])
                self.count['wrong'] += 1
                self.count['last_time']= time.time()
                continue
        # except Exception as e:
        #     print(2*20*'2*')
        #     try:
        #         self.browser.get(self.list[0]['src'])
        #         print(data['src'])
        #         # 模拟输入键盘账号
        #         self.browser.find_element_by_xpath(
        #             '//*[@id="app"]/div/div[2]/form/div[1]/div[1]/input').send_keys(self.username)
        #         self.browser.find_element_by_xpath(
        #             '//*[@id="app"]/div/div[2]/form/div[2]/div/div[1]/input').send_keys(self.password)
        #         self.browser.find_element_by_xpath('//*[@id="denglu"]').click()
        #     except Exception as e:
        #         print(e)
        #     datalist = self.list
        #     for data in datalist:
        #         time.sleep(5*random.random())
        #         itemlist = self.browser.find_elements_by_xpath(
        #             '//*[@id="app"]/div/div[6]/div/div/div[1]/div[1]/div[2]/div/div')
        #         # //*[@id="app"]/div/div[6]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/img
        #         print(len(itemlist))
        #         for item in itemlist:
        #             print(item.find_elements_by_xpath(
        #                 './div/img')[0].get_attribute('src'))
        #         # 货物具体信息
        #         detail = self.browser.find_elements_by_xpath(
        #             '//*[@id="app"]/div/div[6]/div/div/div[1]/div[2]/div')
        #         print(detail)
        #         title = detail[0].find_elements_by_xpath('./span')[0].text
        #         tb_url = detail[0].find_elements_by_xpath(
        #             './a')[0].get_attribute('href')
        #         tb_price = detail[1].find_elements_by_xpath(
        #             './div[2]/div[1]/div/span[2]')[0].text
        #         price = detail[1].find_elements_by_xpath(
        #             './div[2]/div[2]/div/span[2]')[0].text
        #         item_no = detail[2].find_element_by_xpath(
        #             './div[1]/div[2]').text
        #         list_time = detail[2].find_element_by_xpath(
        #             './div[2]/div[2]').text
        #         # color = detail[2].find_element_by_xpath('./div[3]/div[2]/div/div/img').get_attribute('name')
        #         print(tb_price, price, title, tb_url, item_no, list_time)

    def run(self, url):
        self.url = url

        self.get_html()

        while True:
            list = []
            listdata = self.get_data()
            for data in self.list:
                t = threading.Thread(target=self.get_data_detail(), args=(data,)).start()
                list.append(t)
            for tt in list:
                tt.join()
            if self.browser.page_source.find('pn-next disabled') == -1:
                break
            else:
                print('数量', self.i)
                break


if __name__ == '__main__':

    JdSpider().run(
        'https://cs.17zwd.com/shop/3158.htm?spm=7845e869505cd125.48.101.0.0.172456.0')
    JdSpider().run(
        'https://cs.17zwd.com/shop/33818.htm?spm=59258f5bec76a80a.48.101.0.0.289969.0')
    # 两个线程同时运行
    # t1 = threading.Thread(target=spider.run, args=('https://cs.17zwd.com/shop/3158.htm?spm=7845e869505cd125.48.101.0.0.172456.0',))
    # t2 = threading.Thread(target=spider1.run,args=('https://cs.17zwd.com/shop/33818.htm?spm=59258f5bec76a80a.48.101.0.0.289969.0',))
    # t1.start() 
    # t2.start()
    # t1.join()
    # t2.join()
    # print(spider.count)
    # 多进程
    # pool = Pool(processes=2)
    # pool.apply_async(JdSpider().run(
    #     'https://cs.17zwd.com/shop/3158.htm?spm=7845e869505cd125.48.101.0.0.172456.0'))
    # pool.apply_async(JdSpider().run(
    #     'https://cs.17zwd.com/shop/33818.htm?spm=59258f5bec76a80a.48.101.0.0.289969.0'))
    # pool.close()