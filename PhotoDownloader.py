import requests
import random
import re
import time
import os
from bs4 import BeautifulSoup


class GetGirlsPhoto(object):
    def __init__(self, head_url, repository_name):
        self.url = head_url
        self.list_url = []
        self.list_pic_url = dict()
        self.header_file = 'user_agents.txt'
        self.path = repository_name

    #编码问题解决
    def chartset(self, rsp):
        _chart = requests.utils.get_encoding_from_headers(rsp.headers)
        if _chart == 'ISO-8859-1':
            rsp.encoding = requests.utils.get_encodings_from_content(rsp.text)

    #随机User-Agent
    def get_header(self):
        with open(self.header_file, 'r') as f:
            headers = f.readlines()
            header = random.choice(headers).strip()
            header = {'User-Agent': header}
            return header

    #获取首页下方页码列表的链接，存入list_url
    def get_url_list(self):
        rsp = requests.get(self.url, headers=self.get_header())
        self.chartset(rsp)
        tg_bf = BeautifulSoup(rsp.text, 'lxml')
        tag = tg_bf.find_all('a', target='_self')
        res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
        link = re.findall(res_url, str(tag), re.I | re.S | re.M)
        for i in link[1:-3]:
            url = self.url+i
            self.list_url.append(url)
        print('获取\“%s\”子链接成功' % self.url)

    #根据list_url,获取每页的图片入口链接，存入list_pic_url（所有的图片入口链接）
    def get_pic_link(self):
        self.get_url_list()
        for url in self.list_url:
            rsp = requests.get(url, headers=self.get_header())
            self.chartset(rsp)
            tag_bf = BeautifulSoup(rsp.text, 'lxml')
            a_tag = tag_bf.find_all('a', class_='picLink')
            for i in a_tag:
                self.list_pic_url[i.get('title')] = i.get('href')
            time.sleep(1)
            print('获取\“%s\”子链接成功！' % url)

    #根据list_pic_url获取图片详细页的连接，然后分析出图片地址，最后进行下载
    def get_pic(self):
        self.get_pic_link()
        for title, url in self.list_pic_url.items():
            print('开始下载%s系列' % title)
            rsp = requests.get(url, headers=self.get_header()).text
            tag_bf = BeautifulSoup(rsp, 'lxml')
            tag = tag_bf.find('div', class_='pages')
            res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
            link = re.findall(res_url, str(tag), re.I | re.S | re.M)
            dir_path = self.path+'/'+title
            is_exist = os.path.exists(dir_path)
            if not is_exist:
                os.makedirs(dir_path)
            for index, i in enumerate(link[1:-1]):
                real_url = url.rsplit('/', 1)[0]+'/'+i
                if i == "#":
                    rsp = requests.get(url+i, headers=self.get_header())
                else:
                    rsp = requests.get(real_url, headers=self.get_header())
                self.chartset(rsp)
                a_bf = BeautifulSoup(rsp.text, 'lxml')
                img = a_bf.find('div', class_='articleBody')
                res_url = r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')"
                img_url = re.findall(res_url, str(img), re.I | re.S | re.M)
                pic_rsp = requests.get(img_url[0], headers=self.get_header())
                img_name = title+str(index+1)+'.jpg'
                img_path = dir_path+'/'+img_name
                with open(img_path, 'wb') as f:
                    f.write(pic_rsp.content)
                    f.flush()
                f.close()
                print('%s下载完成!' % img_name)
                time.sleep(3)
            print("*" * 30)


if __name__ == '__main__':
    urls = ['http://www.55156.com/a/Mygirl',
            'http://www.55156.com/a/Beautyleg']
    for i in urls:
        url = i
        path_name = i.rsplit('/', 1)[1]
        print(i, path_name)
        pd = GetGirlsPhoto(head_url=url, repository_name=path_name)
        pd.get_pic()
        time.sleep(120)
