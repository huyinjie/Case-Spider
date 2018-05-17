# coding:utf-8
from getProductList import getUrlList
from getProductList import getUrlNamePair

Product_List = []
Product_dict = dict()

getUrlList(Product_List)
getUrlNamePair(Product_List, Product_dict)
print(Product_dict)

