# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re

# Global variables
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


# My definition
# 为爬取到的URL添加前缀
def addPrefix(string):
    string = "https://www.nzxt.com" + string
    return string


# Main Code
def getUrlList(templist):
    url = "https://www.nzxt.com/categories/cases"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", {"class": "category-list-container container"})
    soup = soup.find_all("div", {'class': re.compile("^prod-col$")})

    for link in soup:
        linkUrl = addPrefix(link.h3.a.get('href'))
        templist.append(linkUrl)
    return templist


def getUrlNamePair(tempdict):
    url = "https://www.nzxt.com/categories/cases"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", {"class": "category-list-container container"})
    soup = soup.find_all("div", {'class': re.compile("^prod-col$")})

    for link in soup:
        name = link.h3.get_text().strip()
        linkUrl = addPrefix(link.h3.a.get('href'))
        tempdict[name] = linkUrl
    return tempdict


# Run Test
if __name__ == '__main__':
    Product_List = []
    Product_dict = dict()
    # getUrlList(Product_List)
    # print(Product_List)
    # print(len(Product_List))
    getUrlNamePair(Product_dict)
    print(Product_dict)
    print(len(Product_dict))