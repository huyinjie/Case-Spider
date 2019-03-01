# coding:utf-8
import requests
from bs4 import BeautifulSoup
import json
import translate
import re


# My definition
def haveChinese(word):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(word)

    return match


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


def AttributesAnalysis(tempdict):
    key = list(tempdict.keys())[0]
    value = list(tempdict.values())[0]
    # if key == "五金材质":
    #     return {"Material": translate.ChineseToEnglish(value)}
    if key == "产品尺寸":
        # 匹配 215MM (W) * 336MM (D) * 398MM (H) 和 208MM (W) x 270MM (D) x 372MM (H)
        match1 = re.compile(u"(\d+)MM \(\w\) . (\d+)MM \(\w\) . (\d+)MM \(\w\)")
        # 匹配 195mm (W) x 445 mm (H) x 500 mm (D)
        match2 = re.compile(u"(\d+) ?mm \(\w\) . (\d+) ?mm \(\w\) . (\d+) ?mm \(\w\)")
        # 匹配 250MM (W) *638MM (D) 505MM (H)
        match3 = re.compile(u"(\d+)MM \(\w\) .(\d+)MM \(\w\) (\d+)MM \(\w\)")
        # 匹配 216.4MM (W) * 475.5MM (D) * 497MM (H)
        match4 = re.compile(u"([+-]?([0-9]*[.])?[0-9]+)MM \(\w\) . ([+-]?([0-9]*[.])?[0-9]+)MM \(\w\) . ([+-]?([0-9]*[.])?[0-9]+)MM \(\w\)")
        # 匹配 G3
        match5 = re.compile(u"(\d+)MM（深）×(\d+)MM（高）×(\d+)MM（宽）")

        m1 = match1.search(value)
        m2 = match2.search(value)
        m3 = match3.search(value)
        m4 = match4.search(value)
        m5 = match5.search(value)

        if m1 is not None:
            return {'Width': int(m1.group(1)), 'Depth': int(m1.group(2)), 'Height': int(m1.group(3))}
        if m2 is not None:
            return {'Width': int(m2.group(1)), 'Height': int(m2.group(2)), 'Depth': int(m2.group(3))}
        if m3 is not None:
            return {'Width': int(m3.group(1)), 'Depth': int(m3.group(2)), 'Height': int(m3.group(3))}
        if m4 is not None:
            return {'Width': float(m4.group(1)), 'Depth': float(m4.group(3)), 'Height': float(m4.group(5))}
        if m5 is not None:
            return {'Depth': int(m5.group(1)), 'Height': int(m5.group(2)), 'Width': int(m5.group(3))}
        else:
            return -1
    # G3 有问题
    if key == "五金材质" or key == "a fs fsdf":
        value = translate.ChineseToEnglish(value)
        return {"Material": value}
    if key == "主板支持类型":
        value = value.replace("以内", " Maximum")
        value = value.replace("内", " Maximum")
        return {"Motherboard Support": value}
    # C2有问题
    if key == "驱动器位":
        if haveChinese(value) is not None:
            pass
            value = translate.ChineseToEnglish(value)
        return {"Drive Bays": value}
    if key == "前置接口":
        value = value.replace("麦克风", "Mic")
        value = value.replace("耳机", " Headphone")
        return {"Front I/O": value}
    # elif key == "重量":
        # return {"": float(value.split('：')[1].strip('KG '))}
    # if key == "支持":
    #     key = "显卡支持长度"
    # if key == " 显卡支持长度":
    #     key = "显卡支持长度"
    # elif key == "净重":
    #     key = "重量"
    #     value = "净重：" + value
    # elif key == "支持水冷":
    #     key = "水冷支持"
    # elif key == "外部结构":
    #     key = "五金材质"
    # elif key == "扩展槽":
    #     key = "可支持PCI扩展槽"
    # elif key == "显卡长度支持":
    #     key = "显卡支持长度"
    # elif key == "CPU散热器高度支持":
    #     key = "CPU散热器支持高度"
    else:
        return -1


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

            tempdict['Product name'] = pairlist[x][0]
            # tempdict['Support Color'] = translate.ChineseToEnglish(','.join(pairlist[x][2]))
            tempdict['Support Color'] = (','.join(pairlist[x][2]))

            if AttributesAnalysis(mySplit(specification)) is not -1:
                tempdict.update(AttributesAnalysis(mySplit(specification)))

            # tempdict.update((mySplit(specification)))
        dataList.append(tempdict)
    return dataList


if __name__ == '__main__':
    product_list = [['U1 PLUS', 'http://www.jonsbo.com/products_42_1.html', ['银色', '黑色']], ['U4', 'http://www.jonsbo.com/products_40_1.html', ['银色', '黑色', '蓝色', '金色', '粉色', '红色', '白色']], ['QT03', 'http://www.jonsbo.com/products_38_1.html', ['玻璃版', '静音版', '镜面版']], ['QT01', 'http://www.jonsbo.com/products_10_1c.html', ['黑色版']], ['MOD1', 'http://www.jonsbo.com/products_34_1.html', ['黑红版', '黑绿版']], ['MOD1-MINI', 'http://www.jonsbo.com/products_35_1.html', ['黑红版']], ['VR2', 'http://www.jonsbo.com/products_37_1.html', ['银色版', '黑色版', '红色版']], ['VR1', 'http://www.jonsbo.com/products_33_1.html', ['银色版', '黑色版', '红色版']], ['RM4', 'http://www.jonsbo.com/products_36_1.html', ['银色版', '黑色版']], ['RM3', 'http://www.jonsbo.com/products_30_1.html', ['银色版', '黑色版', '红色版', '深空灰色版', '湖泊蓝色版', '玫瑰粉色版', '香槟金色版']], ['RM2', 'http://www.jonsbo.com/products_29_1.html', ['银色版', '黑色版']], ['W2', 'http://www.jonsbo.com/products_23_1.html', ['银色版', '黑色版', '银色侧透版', '黑色侧透版']], ['UMX5', 'http://www.jonsbo.com/products_50_1.html', ['银色版', '黑色版']], ['UMX4', 'http://www.jonsbo.com/products_31_1.html', ['银色标准版', '银色玻璃侧窗版', '黑色标准版', '黑色玻璃侧窗版']], ['UMX3', 'http://www.jonsbo.com/products_28_1.html', ['银色版', '黑色版', '银色侧透版', '黑色侧透版']], ['UMX1 PLUS', 'http://www.jonsbo.com/products_25_1.html', ['银色版', '黑色版', '侧窗银色版', '侧窗黑色版']], ['C4', 'http://www.jonsbo.com/products_45_1.html', ['白色', '银色', '黑色']], ['C3 PLUS', 'http://www.jonsbo.com/products_56_1.html', ['银色', '黑色']], ['C3', 'http://www.jonsbo.com/products_24_1.html', ['银色版', '黑色版', '银色全侧透版', '黑色全侧透版']], ['C2', 'http://www.jonsbo.com/products_22_1.html', ['银色版', '黑色版', '红色版']], ['U3', 'http://www.jonsbo.com/products_17_1.html', ['银色版', '黑色版', '红色版']], ['U2', 'http://www.jonsbo.com/products_16_1.html', ['银色版', '黑色版', '红色版', 'U2 GAMING龙']], ['U1', 'http://www.jonsbo.com/products_15_1.html', ['银色版', '黑色版', '红色版']], ['V4', 'http://www.jonsbo.com/products_12_1.html', ['银色版', '黑色版', '红色版', '白色版']], ['V3+', 'http://www.jonsbo.com/products_9_1.html', ['银色版', '黑色版', '红色版', '白色版']], ['G3', 'http://www.jonsbo.com/products_4_1.html', ['银色版']]]
    product_data = []
    test_list = [['U1 PLUS', 'http://www.jonsbo.com/products_42_1.html', ['银色', '黑色']]]
    main(product_list, product_data)
    print(product_data)
    with open('jonsbo.json', 'w', encoding='utf8') as json_file:
        data = json.dumps(product_data, ensure_ascii=False, indent=4)
        # unicode(data) auto-decodes data to unicode if str
        json_file.write(str(data))
        print(json_file)
