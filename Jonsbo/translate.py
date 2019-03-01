import requests
import random
import hashlib
import json

appid = '20180601000170782'
secretKey = '9UjP2wlKXu7QcN8hR99T'


def EnglishToChinese(word):
    salt = random.randint(32768, 65536)

    # 生成md5
    text = appid + word + str(salt) + secretKey
    text = text.encode('utf-8')
    text_md5 = hashlib.md5()
    text_md5.update(text)
    text_md5 = text_md5.hexdigest()

    params = {
        'q': word,
        'from': 'en',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign': text_md5,
    }

    response = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', params=params)
    # print(response.url)
    response_text = str(response.text)
    data_json = json.loads(response_text)
    # print(data_json['trans_result'][0]['dst'])
    return data_json['trans_result'][0]['dst']


def ChineseToEnglish(word):
    salt = random.randint(32768, 65536)

    # 生成md5
    text = appid + word + str(salt) + secretKey
    text = text.encode('utf-8')
    text_md5 = hashlib.md5()
    text_md5.update(text)
    text_md5 = text_md5.hexdigest()

    params = {
        'q': word,
        'from': 'zh',
        'to': 'en',
        'appid': appid,
        'salt': salt,
        'sign': text_md5,
    }

    response = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', params=params)
    # print(response.url)
    response_text = str(response.text)
    data_json = json.loads(response_text)
    # print(data_json['trans_result'][0]['dst'])
    return data_json['trans_result'][0]['dst']


if __name__ == '__main__':
    word = "苹果"
    result = ChineseToEnglish(word)
    print(result)

