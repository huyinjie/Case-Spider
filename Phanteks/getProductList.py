# coding:utf-8
import requests
from bs4 import BeautifulSoup

# Global variables
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


# My definition
# 为爬取到的URL添加前缀
def addPrefix(string):
    string = "http://www.phanteks.com/" + string
    return string


# Main Code
def getUrlList(templist):
    url = "http://www.phanteks.com/"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    # soup = soup.find("li", {"class": "megamenu-content"})
    soup = soup.find_all("ul", {"class": "col-lg-2 col-sm-2 col-md-2 unstyled noMarginLeft"})
    for x in soup:
        y = x.find_all("li", id=True)
        for z in y:
            z = z.find_all("a")
            for link in z:
                link.get('href')
                templist.append(addPrefix(link.get('href')))
    return templist


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
    getUrlList(Product_List)
    getUrlNamePair(Product_List, Product_dict)
    print(Product_dict)

