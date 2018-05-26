# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import json


# Global variables
cookies = {
    '_ga': 'GA1.2.10555286.1525853483',
    '__zlcmid': 'mKhKLjsZOL75tm',
    '3060738.3440491': 'da6908cb-1cda-4d5e-99e1-25fa8e5e549c',
    '_gid': 'GA1.2.673263205.1526993580',
    '_my_app_session': 'a38518b4350c1e0808a671f50f5d161a',
    'cart_items_count': '0',
    '_gat': '1',
    '_gat_newTracker': '1',
    '_dc_gtm_UA-1138231-22': '1',
    '_dc_gtm_UA-1138231-10': '1',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.nzxt.com/products/h700-matte-white',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


# My definition
# define a case-like function
def AttributesAnalysis(attribute, data):
    if attribute == 'Dimensions':
        # 匹配 W: 230mm H: 494mm D: 494mm (without feet)
        match1 = re.compile(u"^W: (\d+)\s?mm\s?H: (\d+)\s?mm\s?D: (\d+)\s?mm\s?")
        # 匹配 	220mm x 513mm x 480mm 和 220 x 567 x 544mm
        match2 = re.compile(u"^(\d+)\s?(mm)? x (\d+)\s?(mm)? x (\d+)\s?(mm)?")
        # 匹配 	W: 245 x H: 426 x D: 450mm
        match3 = re.compile(u"^W: (\d+) x H: (\d+) x D: (\d+)")
        # 215mm(W) x 516mm(H) X 532mm(D)
        match4 = re.compile(u"(\d+)mm\(W\) x (\d+)mm\(H\) X (\d+)mm\(D\)")
        m1 = match1.search(data)
        m2 = match2.search(data)
        m3 = match3.search(data)
        m4 = match4.search(data)
        if m1 is not None:
            return {'Width': int(m1.group(1)), 'Height': int(m1.group(2)), 'Depth': int(m1.group(3))}
        elif m2 is not None:
            return {'Width': int(m2.group(1)), 'Height': int(m2.group(3)), 'Depth': int(m2.group(5))}
        elif m3 is not None:
            return {'Width': int(m3.group(1)), 'Height': int(m3.group(2)), 'Depth': int(m3.group(3))}
        elif m4 is not None:
            return {'Width': int(m4.group(1)), 'Height': int(m4.group(2)), 'Depth': int(m4.group(3))}
        else:
            return -1
    elif attribute == 'Form Factor':
        return {'Form Factor': data}
    elif attribute == 'Material(s)':
        return {'Material': data.replace('\n', '')}
    elif attribute == 'Clearance':
        return {'Material': data.replace('\n', '')}
    elif attribute == 'Motherboard Support':
        return {'Motherboard Support': data.replace('\n', '')}
    elif attribute == 'I/O Ports':
        return {'I/O Ports': data.replace('\n', ',')}
    elif attribute == 'Weight':
        return {'Weight': float(data.strip(' kg'))}
    elif attribute == 'Product Weight':
        return {'Weight': float(data.strip(' kg'))}
    # elif attribute == 'Side Window':
    #     return {'Side Window': data.replace('\n', '')}
    else:
        return -1


# main code
def main(pairdict, dataList):
    for k, v in pairdict.items():
        r = requests.get(v, headers=headers, cookies=cookies)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        soup = soup.find("table", {"class": "spec-table table"})
        str(soup).replace("<br/>", " ")
        tempdict = {}
        tempdict.update({'Product name': k})
        for tr in soup:
            # Test
            firsttd_text = tr.td.get_text().strip()
            secondtd_text = tr.find_all("td")[1]
            secondtd_text = ", ".join(secondtd_text.strings)
            # print(firsttd_text, "  ", secondtd_text)
            # print(tr)
            if AttributesAnalysis(firsttd_text, secondtd_text) is not -1:
                tempdict.update(AttributesAnalysis(firsttd_text, secondtd_text))
        dataList.append(tempdict)

    return dataList


# Run Test
if __name__ == '__main__':
    # Product_dict = {'Enthoo Elite': 'http://www.phanteks.com/Enthoo-Elite.html'}
    # Product_List = ['http://www.phanteks.com/Enthoo-Elite.html']
    test = {'H700': 'https://www.nzxt.com/products/h700-matte-white'}
    test2 = {'H700': 'https://www.nzxt.com/products/h700-matte-white', 'H500': 'https://www.nzxt.com/products/h500-matte-white', 'H400': 'https://www.nzxt.com/products/h400-matte-white', 'H200': 'https://www.nzxt.com/products/h200-matte-white', 'H700i': 'https://www.nzxt.com/products/h700i-matte-white', 'H500i': 'https://www.nzxt.com/products/h500i-matte-white', 'H400i': 'https://www.nzxt.com/products/h400i-matte-white', 'H200i': 'https://www.nzxt.com/products/h200i-matte-white', 'H700i Ninja': 'https://www.nzxt.com/products/h700i-ninja', 'H700 PUBG': 'https://www.nzxt.com/products/h700-pubg-limited-edition', 'S340 Elite': 'https://www.nzxt.com/products/s340-elite-matte-white', 'S340': 'https://www.nzxt.com/products/s340-white', 'H440': 'https://www.nzxt.com/products/h440-white', 'Manta': 'https://www.nzxt.com/products/manta-matte-white-black', 'Noctis 450': 'https://www.nzxt.com/products/noctis-450-white-blue', 'Source 530': 'https://www.nzxt.com/products/source-530', 'Phantom 410': 'https://www.nzxt.com/products/phantom-410-white', 'Phantom': 'https://www.nzxt.com/products/phantom-white', 'Phantom 530': 'https://www.nzxt.com/products/phantom-530', 'H440 Hyper Beast': 'https://www.nzxt.com/products/h440-hyper-beast', 'S340 Elite Hyper Beast': 'https://www.nzxt.com/products/s340-elite-hyper-beast', 'H440 - Designed by Razer™': 'https://www.nzxt.com/products/h440-designed-by-razer', 'S340 - Designed by Razer™': 'https://www.nzxt.com/products/s340-designed-by-razer', 'S340 Elite Limited Purple Edition': 'https://www.nzxt.com/products/s340-elite-limited-purple-edition', 'Noctis 450 ROG': 'https://www.nzxt.com/products/noctis-450-rog'}

    Product_Data = []
    main(test2, Product_Data)
    print(Product_Data)

    # Write Json
    json_str = json.dumps(Product_Data, indent=4)
    with open('nzxt.json', 'w') as outfile:
        outfile.write(json_str)
    print(json_str)



