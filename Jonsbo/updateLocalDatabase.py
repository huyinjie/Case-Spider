# coding=gbk

import pymongo


def main(templist):
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client['test']

    collection = db['jonsbo']
    result = collection.drop()
    result = collection.insert_many(templist)
    print(result)

