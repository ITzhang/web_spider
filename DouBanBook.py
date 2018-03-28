#!-*-coding:utf-8-*-
import requests
import xlwt
from bs4 import BeautifulSoup
from collections import OrderedDict


class DouBanBookSpider(object):

    def __init__(self, book_type, quantity):
        self.book_type = book_type
        self.quantity = quantity
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebK'
                                     'it/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
        self.url_list = []
        self.book_dict = OrderedDict()
        self.count = 0

    #获取url
    def get_url(self):
        count = 0
        while count < self.quantity+1:
            url = 'https://book.douban.com/tag/%s?start=%d&type=S' % (self.book_type, count)
            self.url_list.append(url)
            #每页20本书，
            count += 20
        return self.url_list

    #爬虫主体
    def main_spider(self, url):
        rsp = requests.get(url, headers=self.header)
        tag_bf = BeautifulSoup(rsp.text, 'lxml')
        content = tag_bf.find_all('li', class_='subject-item')
        if content:
            for i in content:
                bt_bf = BeautifulSoup(str(i), 'lxml')
                self.count += 1
                book_name = bt_bf.h2.a.get_text(strip=True)
                author = bt_bf.find('div', class_='pub').string.strip()
                comment_info = bt_bf.find('div', class_='star clearfix')
                co_bf = BeautifulSoup(str(comment_info), 'lxml')
                grade = co_bf.find('span', class_='rating_nums')
                if grade:
                    grade = grade.string
                comment_count = co_bf.find('span', class_='pl').string.strip()
                self.book_dict[str(self.count)] = {'序号': self.count, '书名': book_name, '评分': grade, '评论数': comment_count, '作者': author}
        else:
            return

    #执行爬虫
    def do_spider(self):
        for i in self.get_url():
            self.main_spider(i)

    #数据写入excel
    def write_excel(self):
        wb = xlwt.Workbook(encoding='ascii')
        ws = wb.add_sheet(self.book_type)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        style.font = font
        row0 = ['序号', '书名', '评分', '评论数', '出版信息']
        for i in range(0, len(row0)):
            ws.write(0, i, row0[i], style)
        for k, v in self.book_dict.items():
            for j in range(0, len(v.values())):
                ws.write(int(k), j, list(v.values())[j])
        wb.save('豆瓣图书分类之%s.xlsx' % self.book_type)


if __name__ == "__main__":
    ds = DouBanBookSpider('科幻小说', 200)
    ds.do_spider()
    ds.write_excel()






