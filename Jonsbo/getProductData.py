# coding:utf-8
import requests
from bs4 import BeautifulSoup
import json


# My definition
def mySplit(string):
    former_array = ''
    latter_array = ''
    k = 0
    for x in range(len(string)):
        if k == 1:
            latter_array = latter_array + string[x]
        if string[x] == '：':
            k = 1
        if k == 0:
            former_array = former_array + string[x]
    return {former_array: latter_array}


def deldict(tempdict):
    if '面板部分材质' in tempdict:
        del tempdict['面板部分材质']
    if '五金部分材质' in tempdict:
        del tempdict['五金部分材质']
    if '风扇调速器位' in tempdict:
        del tempdict['风扇调速器位']
    if '五金特色配件' in tempdict:
        del tempdict['五金特色配件']
    if '面板特色配件' in tempdict:
        del tempdict['面板特色配件']
    if '面板材质' in tempdict:
        del tempdict['面板材质']


def cleanData(tempdict):
    k = list(tempdict.keys())[0]
    v = list(tempdict.values())[0]
    if k == "支持":
        k = "显卡支持长度"
    if k == " 显卡支持长度":
        k = "显卡支持长度"
    elif k == "净重":
        k = "重量"
        v = "净重：" + v
    elif k == "支持水冷":
        k = "水冷支持"
    elif k == "外部结构":
        k = "五金材质"
    elif k == "扩展槽":
        k = "可支持PCI扩展槽"
    elif k == "显卡长度支持":
        k = "显卡支持长度"
    elif k == "CPU散热器高度支持":
        k = "CPU散热器支持高度"
    return {k: v}


# main code
def main(pairlist, dataList):
    for x in range(len(pairlist)):
        v = pairlist[x][1]
        r = requests.get(v)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        soup = soup.find_all("div", {"id": "productid"})
        soup = soup[1]
        soup = soup.table.tr.td.table

        tempdict = {}
        for specification in soup.find_all("td", text=True):
            specification = specification.find('a').text

            # if cleanData(mySplit(specification)) is not None:
            #     tempdict.update(cleanData(mySplit(specification)))

            tempdict.update(cleanData(mySplit(specification)))
            tempdict['颜色'] = (','.join(pairlist[x][2]))
            tempdict['产品型号'] = pairlist[x][0]
            deldict(tempdict)
        dataList.append(tempdict)
    return dataList


if __name__ == '__main__':
    product_list = [['U1 PLUS', 'http://www.jonsbo.com/products_42_1.html', ['银色', '黑色']], ['U4', 'http://www.jonsbo.com/products_40_1.html', ['银色', '黑色', '蓝色', '金色', '粉色', '红色', '白色']], ['QT03', 'http://www.jonsbo.com/products_38_1.html', ['玻璃版', '静音版', '镜面版']], ['QT01', 'http://www.jonsbo.com/products_10_1c.html', ['黑色版']], ['MOD1', 'http://www.jonsbo.com/products_34_1.html', ['黑红版', '黑绿版']], ['MOD1-MINI', 'http://www.jonsbo.com/products_35_1.html', ['黑红版']], ['VR2', 'http://www.jonsbo.com/products_37_1.html', ['银色版', '黑色版', '红色版']], ['VR1', 'http://www.jonsbo.com/products_33_1.html', ['银色版', '黑色版', '红色版']], ['RM4', 'http://www.jonsbo.com/products_36_1.html', ['银色版', '黑色版']], ['RM3', 'http://www.jonsbo.com/products_30_1.html', ['银色版', '黑色版', '红色版', '深空灰色版', '湖泊蓝色版', '玫瑰粉色版', '香槟金色版']], ['RM2', 'http://www.jonsbo.com/products_29_1.html', ['银色版', '黑色版']], ['W2', 'http://www.jonsbo.com/products_23_1.html', ['银色版', '黑色版', '银色侧透版', '黑色侧透版']], ['UMX5', 'http://www.jonsbo.com/products_50_1.html', ['银色版', '黑色版']], ['UMX4', 'http://www.jonsbo.com/products_31_1.html', ['银色标准版', '银色玻璃侧窗版', '黑色标准版', '黑色玻璃侧窗版']], ['UMX3', 'http://www.jonsbo.com/products_28_1.html', ['银色版', '黑色版', '银色侧透版', '黑色侧透版']], ['UMX1 PLUS', 'http://www.jonsbo.com/products_25_1.html', ['银色版', '黑色版', '侧窗银色版', '侧窗黑色版']], ['C4', 'http://www.jonsbo.com/products_45_1.html', ['白色', '银色', '黑色']], ['C3 PLUS', 'http://www.jonsbo.com/products_56_1.html', ['银色', '黑色']], ['C3', 'http://www.jonsbo.com/products_24_1.html', ['银色版', '黑色版', '银色全侧透版', '黑色全侧透版']], ['C2', 'http://www.jonsbo.com/products_22_1.html', ['银色版', '黑色版', '红色版']], ['U3', 'http://www.jonsbo.com/products_17_1.html', ['银色版', '黑色版', '红色版']], ['U2', 'http://www.jonsbo.com/products_16_1.html', ['银色版', '黑色版', '红色版', 'U2 GAMING龙']], ['U1', 'http://www.jonsbo.com/products_15_1.html', ['银色版', '黑色版', '红色版']], ['V4', 'http://www.jonsbo.com/products_12_1.html', ['银色版', '黑色版', '红色版', '白色版']], ['V3+', 'http://www.jonsbo.com/products_9_1.html', ['银色版', '黑色版', '红色版', '白色版']], ['G3', 'http://www.jonsbo.com/products_4_1.html', ['银色版']]]
    product_data = []
    main(product_list, product_data)
    print(product_data)
    with open('jonsbo.json', 'w', encoding='utf8') as json_file:
        data = json.dumps(product_data, ensure_ascii=False, indent=4)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(str(data))
        print(json_file)
