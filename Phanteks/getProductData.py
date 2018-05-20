# coding:utf-8
import requests
from bs4 import BeautifulSoup

# Global variables
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


# main code
def main(pairlist, dataList):
    for x in range(len(pairlist)):
        v = pairlist[x]
        r = requests.get(v, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        soup = soup.find("table")
        # soup = soup.tbody
        soup = soup.find_all("tr")[5:11]
        for tr in soup:
            firsttd_text = tr.td.div.get_text().strip()
            secondtd_text = tr.find_all("td")[1].div.get_text().strip()
            print(firsttd_text)
            print(secondtd_text)
            print('')

        # soup = soup.find_all("div", {"id": "productid"})
    return dataList


# Run Test
if __name__ == '__main__':
    Product_dict = {'Enthoo Elite': 'http://www.phanteks.com/Enthoo-Elite.html'}
    Product_List = ['http://www.phanteks.com/Enthoo-Elite.html']
    Product_Data = []
    main(Product_List, Product_Data)
    # print(Product_dict)
