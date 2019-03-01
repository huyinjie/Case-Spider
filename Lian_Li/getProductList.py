# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re


# Global variables
serial_list = ["http://www.lian-li.com/small/",
               "http://www.lian-li.com/medium/",
               "http://www.lian-li.com/large/"]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


# My definition
# 为爬取到的URL添加前缀
def addPrefix(string):
    string = "http://www.phanteks.com/" + string
    return string


# Main Code
def getUrlList(templist, url):
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", {"class": "mkd-full-width-inner"})
    print(soup)
    # soup = soup.fina_all("a", href=re.compile("^http://www.lian-li.com/"))
    print(soup)
    # for x in soup:
    #     link = x.div.div.div.figure.a.get('href')
    #     link = link.strip(' /')
    #     print(link)

# def getUrlList(templist, url):
#     r = requests.get(url, headers=headers)
#     r.encoding = 'utf-8'
#     soup = BeautifulSoup(r.text, "lxml")
#     soup = soup.find_all("div", {"class": "wpb_column vc_column_container vc_col-sm-3"})
#     for x in soup:
#         link = x.div.div.div.figure.a.get('href')
#         link = link.strip(' /')
#         print(link)
        # y = x.find_all("li", id=True)
    #     for z in y:
    #         z = z.find_all("a")
    #         for link in z:
    #             link.get('href')
    #             templist.append(addPrefix(link.get('href')))
    # return templist


def getUrlNamePair(templist, tempdict):
    for url in templist:
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        soup = soup.find("h1", {"class": "product-title"})
        tempdict[soup.get_text().strip()] = url
    return tempdict


# Run Test
if __name__ == '__main__':
    Product_List = []
    Product_dict = dict()
    # for urls in serial_list:
    #     getUrlList(Product_List, urls)
    getUrlList(Product_List, serial_list[0])
    # getUrlNamePair(Product_List, Product_dict)
    # for item in Product_dict.items():
    #     print(item)
    # print(len(Product_dict))
    # # print(Product_List)
