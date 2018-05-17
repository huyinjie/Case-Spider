from Phanteks.getProductList import getUrlNamePair
from Phanteks.getProductList import getUrlList


Product_List = []
Product_dict = dict()

getUrlList(Product_List)
getUrlNamePair(Product_List, Product_dict)
print(Product_dict)

