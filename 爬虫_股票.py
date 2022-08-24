# 导入相关库
import requests
from bs4 import BeautifulSoup
import pandas as pd
from snownlp import SnowNLP


# 请求数据，定义函数
def getHTMLText(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    text = r.text
    return text


# 解析单个网页，并提取数据字段
def getOnePageInfo(url):
    one_page_data = []
    text = getHTMLText(url)
    soup = BeautifulSoup(text, 'html.parser')
    post_list = soup.find_all('div', class_="articleh normal_post")
    for post in post_list:
        read_counts = post.find('span', class_="l1 a1").text
        comment_counts = post.find('span', class_="l2 a2").text
        title = post.find('span', class_="l3 a3").text
        author_id = post.find('span', class_="l4 a4").text
        time = post.find('span', class_="l5 a5").text
        data = [read_counts, comment_counts, title, author_id, time]
        one_page_data.append(data)
    return one_page_data


# 循环获得多页信息（以1-10页为例）
all_data = []
for i in range(1, 11):
    url = f'https://guba.eastmoney.com/list,zssh000001_{i}.html'
    one_page_data = getOnePageInfo(url)
    all_data.extend(one_page_data)  # extend可以添加列表

# print(all_data)
# 将数据存储至csv文件中
all_data = pd.DataFrame(all_data, columns=['阅读数', '评论数', '标题', '作者', '最后更新'])
all_data.to_csv(r'D:\work\1 bs\000001帖子.csv')


def senti(text):
    s = SnowNLP(text)
    return s.sentiments


all_data['情绪'] = all_data['标题'].apply(senti)
all_data.to_csv(r'D:\work\1 bs\000001帖子+情感.csv')
