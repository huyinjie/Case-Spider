import getProductList

Product_List = []
Product_dict = dict()

getProductList.getUrlList(Product_List)
getProductList.getUrlNamePair(Product_List, Product_dict)
print(Product_dict)

