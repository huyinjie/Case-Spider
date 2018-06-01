# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup


# My definition
# 为爬取到的URL添加前缀
def addPrefix(string):
    string = "http://www.jonsbo.com/" + string
    return string


# 从list中提取产品颜色
def colorClean(templist):
    for k in range(len(templist)):
        text = templist[k]
        colormatch = (re.compile(u"[\u4e00-\u9fa5]+"u"\u8272")).search(text)
        versionmatch = (re.compile(u"[\u4e00-\u9fa5]+"u"\u7248")).search(text)
        mixmatch = (re.compile(u"[\u4e00-\u9fa5]+"u"\u8272"u"\u7248")).search(text)

        if mixmatch:
            templist[k] = mixmatch.group()
        elif versionmatch:
            templist[k] = versionmatch.group()
        elif colormatch:
            templist[k] = colormatch.group()
    return templist


# 从字符串提取型号
def getSortName(string):
    string = (string.split('专区'))[0]
    return string


# My main code
# 传入一个空dict
# 返回该dict，key为型号，value为url
def getNameUrlPair(tempdict):
    url = "http://www.jonsbo.com/index.html"
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("ul", {"id": "subMenu26"})
    soup = soup.find_all("li")
    for li in soup:
        k = li.a.get_text()
        v = addPrefix(li.a.get('href'))
        tempdict[k] = v
    return tempdict


# 传入一个getNameUrlPair函数返回的dict和一个空list
# 返回该list，该list为二维数组，其中每个型号的型号名，url，拥有的颜色分别为list[i][0~2]

# def getNameUrlColorPair(tempdict, templist):
#     index = 0
#     for k, v in tempdict.items():
#         singleList = [[], [], []]
#         r = requests.get(v)
#         r.encoding = 'utf-8'
#         soup = BeautifulSoup(r.text, "lxml")
#
#         firstlink = soup.find("td", {"id": "pic_txt"})
#         firstlink = firstlink.a.get('href')
#         singleList[1] = addPrefix(firstlink)
#         singleList[0] = getSortName(k)
#         for item in soup.find_all("td", {"id": "pic_txt"}):
#             for link in item.find_all('a', href=re.compile("^products_\d")):
#                 singleList[2].append(link.get_text())
#         singleList[2] = colorClean((singleList[2]))
#         templist[index] = singleList
#         index = index + 1
#     return templist


def getNameUrlColorPair(tempdict, templist):
    url = "http://www.jonsbo.com/index.html"
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")

    soup = soup.find("ul", {"id": "subMenu26"})
    soup = soup.find_all("li")
    for li in soup:
        k = li.a.get_text()
        v = addPrefix(li.a.get('href'))
        tempdict[k] = v
    index = 0
    for k, v in tempdict.items():
        singleList = [[], [], []]
        r = requests.get(v)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")

        firstlink = soup.find("td", {"id": "pic_txt"})
        firstlink = firstlink.a.get('href')
        singleList[1] = addPrefix(firstlink)
        singleList[0] = getSortName(k)
        for item in soup.find_all("td", {"id": "pic_txt"}):
            for link in item.find_all('a', href=re.compile("^products_\d")):
                singleList[2].append(link.get_text())
        singleList[2] = colorClean((singleList[2]))
        templist[index] = singleList
        index = index + 1
    return templist


if __name__ == '__main__':
    product_url_dict = dict()
    product_url_dict = getNameUrlPair(product_url_dict)
    product_url_color_list = [None] * len(product_url_dict.items())
    product_url_color_list = getNameUrlColorPair(product_url_dict, product_url_color_list)
    print(product_url_color_list)


