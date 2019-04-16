# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import re

class downloader(object):

    def __init__(self):
        self.server = 'https://www.publico.pt'
        self.page_server = 'https://www.publico.pt/tecnologia?page='
        self.target = 'https://www.publico.pt/tecnologia'
        self.names = []  # 存放文章名
        self.urls = []  # 存放文章链接
        self.nums = 0  # 章节数

        self.page_urls = []   # 存放页面链接
    """
    函数说明:获取页面
    """
    def get_page_url(self):
        # 获取页面链接
        page_num_begin = int(input(("Enter page_num_begin: ")))   # 输入爬取页面起始页数
        page_num_end = int(input(("Enter page_num_end: ")))  # 输入爬取页面结束页数
        page_num = page_num_end - page_num_begin + 1
        if page_num <= 0:
            print("输入无效结束页必须大于起始页")
        print("爬取页面数：", page_num)
        if page_num_begin > 1:
            while page_num_begin <= page_num_end:
                self.page_urls.append(self.page_server + str(page_num_begin))
                page_num_begin = page_num_begin + 1
        else:
            self.page_urls.append(self.target)
            page_num_begin = page_num_begin + 1
            while page_num_begin <= page_num_end:
                self.page_urls.append(self.page_server + str(page_num_begin))
                page_num_begin = page_num_begin + 1
        print(self.page_urls)

    """
     函数说明:获取文章标题及下载链接
     """

    def get_download_url(self):
        titlelinkall = []
        titlelistall =[]
        linksall =[]
        for each in range(len(self.page_urls)):
            titlelink = []
            # print(self.page_urls[each])
            req = requests.get(url=self.page_urls[each])
            html = req.text
            div_bf = BeautifulSoup(html, 'html.parser')
            div = div_bf.find_all('div', class_='page__body')
            # 获取标题
            titlelist = []
            div1_bf = BeautifulSoup(str(div), 'html.parser')
            headlinetitle = div1_bf.find_all('h3')  # 头条文章标题
            ul = div1_bf.find('ul', class_='headline-list headline-list--ordered')
            headlisttitle_bf = BeautifulSoup(str(ul), 'html.parser')
            headlisttitle = headlisttitle_bf.find_all('h4')  # 文章列表标题
            if len(headlisttitle)| len(headlinetitle) > 0:   # 判断是否存在文章标题（有标题必然存在文章内容），不存在直接结束
                titlelist.append(re.sub('\n|\r', '', headlinetitle[0].text))
                for each in headlisttitle:
                    titlelist.append(re.sub('\n|\r', '', each.text))
                # 获取文章链接
                headlinelink = div1_bf.find_all('a', class_='card__faux-block-link')
                # print(self.server + headlinelink[0].get('href'))
                parserlink = div1_bf.find_all('div', class_='media-object-section')
                linklist_bf = BeautifulSoup(str(parserlink), 'html.parser')
                linklist = linklist_bf.find_all('a')
                links = []
                for each in range(len(linklist)):
                    web = linklist[each].get('href')  # 获取所有链接
                    links.append(web)
                linksnew = []
                for each in range(len(links)):
                    matchObj1 = links[each].find("comments")  # 去除comments链接
                    if matchObj1 < 0:
                        linksnew.append(links[each])

                linksnew1 = []
                linksnew1.append(self.server + headlinelink[0].get('href'))
                for each in range(len(linksnew)):
                    matchObj2 = linksnew[each].find("autor")  # 去除autor链接
                    if matchObj2 < 0:
                        linksnew1.append(self.server + linksnew[each])

                # 整合输出标题及文章链接
                # print(linksnew1, len(linksnew1),len(titlelist))
                for each in range(len(linksnew1)):
                    titlelink.append(titlelist[each] + ' ' + linksnew1[each])
                # print(titlelink)
                for each in range(len(titlelink)):
                    titlelistall.append(titlelist[each])
                    linksall.append(linksnew1[each])
                    titlelinkall.append(titlelink[each])
        self.nums = len(titlelinkall)  # 并统计章节数
        for each in range(len(titlelinkall)):
            self.names.append(titlelistall[each])
            self.urls.append(linksall[each])
            # print(self.names[each], self.urls[each])
        # print(self.urls)

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    """

    def get_contents (self, target):
        req = requests.get(url=target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')
        div = div_bf.find_all('div', class_='content')
        p_bf = BeautifulSoup(str(div), 'html.parser')
        p = p_bf.find_all('p')
        # 问题：怎么把元组多个元素组成一个
        contents = []
        for each in range(len(p)):
            contents.append(re.sub('\n|\r', '', p[each].text))
            # print(contents)
            texts = ''.join(contents)   # 元组中多个元素组合
            # texts = line.encode('GBK', 'ignore').decode('GBK', 'ignore')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,文章保存名称(string)
        text - 章节内容(string)
    """

    def writer (self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(name) + '\n')
            f.writelines(text)
            f.write('\n\n')

if  __name__ == "__main__":
    dl = downloader()
    dl.get_page_url()
    dl.get_download_url()
    print('文章开始下载')
    print('共计文章数目：', dl.nums)
    if dl.nums > 0:   # 判断文章是否存在，也即判断是否可以写入文本生成文件
        for i in range(dl.nums):
            dl.writer(dl.names[i], 'Paper.txt', dl.get_contents(dl.urls[i]))
            # print(dl.names[i], dl.get_contents(dl.urls[i]))
            # sys.stdout.write("  已下载:%.3f%%" % float(i / dl.nums) + '\r')
            # sys.stdout.flush()
        print("文章下载完成")
        # 计算单词数
        contents = open('Paper.txt', 'r', encoding='UTF-8').read()
        contents = re.sub(r'[^\w\s]', ' ', contents)  # 去除标点符号
        contents = contents.split()  # 以单词间空格分隔
        Word_num = len(contents)
        print("文章数目：%s,\n共计单词数：%s" % (dl.nums, Word_num))

        # 生成文本词频表
        contentsword = []
        for each in range(len(contents)):  # 把大写字母变为小写
            contentsword.append(str(contents[each]).lower())
        w = open('Wordscount.txt', 'w', encoding='utf-8')
        map = {}
        for word in contentsword:  # 计算每个单词数量
            map[word] = map[word] + 1 \
                if word in map.keys() \
                else 1
        map = sorted(map.items(), key=lambda item: item[1], reverse=True)  # 倒序，注意这里map变为列表
        words_num = len(map)
        w.writelines('单词种类：%s\n' % words_num)
        print("单词种类:%s" % words_num)
        # print(map)
        for key in range(len(map)):  # 写入text文件
            texts = map[key]
            w.writelines(str(texts) + '\n')
        w.close()

        WordsList = open('WordList.txt', 'r',encoding='utf-8').read()  # 读取需匹配的单词表
        WordsList = re.split('\n', WordsList)  # 分割换行符以元组形式存储备用

        # 统计给定单词表的出现次数
        f = open('result.txt', 'w', encoding='utf-8')
        f.writelines("统计结果如下:\n文章数目：%s\n共计单词数：%s\n单词种类数：%s\n" % (dl.nums, Word_num, words_num))
        for each in range(len(WordsList)):  # 第一层是单词表的循环
            a = 0
            for line in range(Word_num):
                Word = WordsList[each]
                matchObj = re.fullmatch(Word, contents[line], re.M | re.I)  # 第二层是在下载的文本中每行匹配相应的单词,已忽略大小写
                if matchObj:
                    a = a + 1  # 计数
            result = Word + ':' + str(a)
            print(result)  # 打印输出
            f.writelines(result + '\n')  # 写入文本
        f.close()
    else:
        print("爬取页面无文章")
