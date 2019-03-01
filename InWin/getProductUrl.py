import requests
import re
from bs4 import BeautifulSoup

ComputerChassisUrl = "https://www.in-win.com/en/computer-chassis/list/28/APAC"  # Computer Chassis
GamingChassisUrl = "https://www.in-win.com/en/gaming-chassis"  # Gaming Chassis

getProductData = ["https://www.in-win.com/en/computer-chassis/bq-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/bm-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/bp-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/bl-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/ce-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/bk-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/ef-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/efs-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/z-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/em-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/c-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/bw-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/ea-series/APAC",
                  "https://www.in-win.com/en/computer-chassis/pe-series/APAC"]
# bq~bp:Mini-ITX  bl~em:Micro-ATX  c~pe:ATX


# My main code
# 返回一个dict
def get_ComputerChassis_Url(url, Product_Data_List):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find("div", {"class": "slick-track"})
    for item in soup.find_all("li"):
        print(item)
        # for link in item.find_all('a', href=re.compile("^products_\d")):
        #     Product_Data_List[link.get_text()] = link.get('href')

    return Product_Data_List


r = requests.get("https://www.in-win.com/en/computer-chassis/bm-series/APAC#product_spec")
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, "lxml")
print(soup)
soup = soup.find_all("div", class_="slick-track")
# print(soup)
# for item in soup.find_all("li"):
#     print(item)

