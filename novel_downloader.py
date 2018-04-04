# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys


class DownLoader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/0_790/'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebK'
                                     'it/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
        self.name = []
        self.urls = []
        self.num = 0

    def get_downloader_url(self):
        req = requests.get(url=self.target, headers=self.header)
        html = req.text
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')
        a = a_bf.find_all('a')
        self.num = len(a[16:])
        for i in a[16:]:
            self.name.append(i.string)
            self.urls.append(self.server+i.get('href'))

    def get_content(self, target):
        req = requests.get(target, headers=self.header)
        print(requests.utils.get_encoding_from_headers(req.headers))
        html = req.text
        con_bf = BeautifulSoup(html, 'lxml')
        con = con_bf.find_all('div', class_='showtxt')
        con = con[0].text.replace('\xa0'*8, '\n\n')
        return con

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == '__main__':
    dl = DownLoader()
    dl.get_downloader_url()
    print('《元尊》开始下载：')
    for i in range(dl.num):
        dl.writer(dl.name[i], '元尊.txt', dl.get_content(dl.urls[i]))
        sys.stdout.write("已下载：%.3f" % float(i/dl.num)+'\r')
        sys.stdout.flush()
    print('下载完成')

