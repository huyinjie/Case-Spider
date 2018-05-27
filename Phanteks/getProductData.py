# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import json


# Global variables
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


# My definition
# define a case-like function
def AttributesAnalysis(attribute, data):
    if attribute == 'Dimension':
        m = re.compile(u"^(\d+)\s?mm x (\d+)\s?mm x (\d+)\s?mm").search(data)
        return {'Width': int(m.group(1)), 'Height': int(m.group(2)), 'Depth': int(m.group(3))}
    # elif attribute == 'Form Factor':
    #     return {'Form Factor': data}
    elif attribute == 'Material(s)':
        return {'Material': data.replace('\n', '')}
    elif attribute == 'Materials':
        return {'Material': data.replace('\n', '')}
    elif attribute == 'Motherboard Support':
        return {'Motherboard Support': data.replace('\n', '')}
    elif attribute == 'Front I/O':
        return {'Front I/O': data.replace('\n', '')}
    # elif attribute == 'Side Window':
    #     return {'Side Window': data.replace('\n', '')}
    else:
        return -1


# main code
def main(pairdict, dataList):
    for k, v in pairdict.items():
        r = requests.get(v, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        soup = soup.find("table")
        # soup = soup.tbody
        soup = soup.find_all("tr")[5:14]
        tempdict = {}

        tempdict.update({'Product name': k})
        for tr in soup:
            try:
                firsttd_text = tr.td.div.get_text().strip()
            except:
                pass

            try:
                secondtd_text = tr.find_all("td")[1].div.get_text().strip()
            except:
                pass

            if AttributesAnalysis(firsttd_text, secondtd_text) is not -1:
                tempdict.update(AttributesAnalysis(firsttd_text, secondtd_text))
        dataList.append(tempdict)

        # print(tempdict)
        # print('')
    return dataList


# Run Test
if __name__ == '__main__':
    # Product_dict = {'Enthoo Elite': 'http://www.phanteks.com/Enthoo-Elite.html'}
    # Product_List = ['http://www.phanteks.com/Enthoo-Elite.html']
    test = {'Enthoo Elite': 'http://www.phanteks.com/Enthoo-Elite.html'}
    test2 = {'Enthoo Elite': 'http://www.phanteks.com/Enthoo-Elite.html', 'Enthoo Primo': 'http://www.phanteks.com/Enthoo-Primo.html', 'Enthoo Primo Special Edition': 'http://www.phanteks.com/Enthoo-Primo-SE.html', 'Enthoo Luxe': 'http://www.phanteks.com/Enthoo-Luxe.html', 'Enthoo Luxe Tempered Glass': 'http://www.phanteks.com/Enthoo-Luxe-TemperedGlass.html', 'Enthoo Pro': 'http://www.phanteks.com/Enthoo-Pro.html', 'Enthoo Pro Tempered Glass': 'http://www.phanteks.com/Enthoo-Pro-TemperedGlass.html', 'Enthoo Pro  Tempered Glass': 'http://www.phanteks.com/Enthoo-Pro-SpecialEdition.html', 'Enthoo Evolv ATX': 'http://www.phanteks.com/Enthoo-Evolv-ATX.html', 'Enthoo Evolv ATX Glass': 'http://www.phanteks.com/Enthoo-Evolv-ATX-TemperedGlass.html', 'Enthoo Pro M': 'http://www.phanteks.com/Enthoo-Pro-M.html', 'Enthoo Pro M Acrylic': 'http://www.phanteks.com/Enthoo-Pro-M-Acrylic.html', 'Enthoo Pro M Tempered Glass': 'http://www.phanteks.com/Enthoo-Pro-M-SpecialEdition.html', 'Enthoo Mini XL DS': 'http://www.phanteks.com/Enthoo-MiniXL-DS.html', 'Enthoo Mini XL': 'http://www.phanteks.com/Enthoo-MiniXL.html', 'Enthoo Evolv mATX Tempered Glass': 'http://www.phanteks.com/Enthoo-Evolv-mATX-TemperedGlass.html', 'Enthoo Evolv ITX': 'http://www.phanteks.com/Enthoo-Evolv-ITX.html', 'Enthoo Evolv ITX Tempered Glass': 'http://www.phanteks.com/Enthoo-Evolv-ITX-TemperedGlass.html', 'Enthoo Evolv Shift x': 'http://www.phanteks.com/Enthoo-Evolv-Shift-X.html', 'Enthoo Evolv Shift': 'http://www.phanteks.com/Enthoo-Evolv-Shift.html', 'Eclipse p400': 'http://www.phanteks.com/Eclipse-P400.html', 'Eclipse P400 Tempered Glass': 'http://www.phanteks.com/Eclipse-P400-TemperedGlass.html', 'Eclipse p400S': 'http://www.phanteks.com/Eclipse-P400S.html', 'Eclipse P400S Tempered Glass': 'http://www.phanteks.com/Eclipse-P400S-TemperedGlass.html', 'Eclipse P300 Tempered Glass': 'http://www.phanteks.com/Eclipse-P300-TemperedGlass.html'}

    Product_Data = []
    main(test2, Product_Data)
    # print(Product_Data)
    json_str = json.dumps(Product_Data, indent=4)
    with open('phanteks.json', 'w') as outfile:
        outfile.write(json_str)
    print(json_str)



