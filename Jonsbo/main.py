# coding:utf-8
import getProductData
import updateLocalDatabase
import getProductList

Product_Sort_Dict = dict()
Product_List = [None]*26
Parameter_List = []

Product_Parameter = ['产品型号', '颜色', '产品尺寸', '主板支持类型', 'CPU散热器支持高度', '显卡支持长度', '五金材质', '面板材质', '驱动器位', '前置接口', '散热系统', '风扇调速器位', '扩展槽', '电源支持', '重量']

Product_Sort_Dict = getProductList.getNameUrlPair(Product_Sort_Dict)

Product_List = getProductList.getNameUrlColorPair(Product_Sort_Dict, Product_List)
Parameter_List = getProductData.main(Product_List, Parameter_List)
print("Successfully!")
# updateDatabase.main(Parameter_List)

