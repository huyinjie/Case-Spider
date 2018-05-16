# coding:utf-8
import requests
from bs4 import BeautifulSoup


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

