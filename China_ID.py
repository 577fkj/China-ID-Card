import requests
from lxml import etree
import time
import json
import random
import datetime

js = json.loads(open('./china_id.json','r').read())

def get(l):
    """
    获取数据库没有的区号*免责声明:仅供学习参考禁止违法犯罪
    """
    try:
        html = requests.get('http://www.stl56.com/idcard/'+str(l)+'.html').text
    except Exception as e:
        print(e)
        return ''
    else:
        html = etree.HTML(html)
        xpath = html.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/h2')
        if len(xpath) != 0:
            return xpath[0].text
        else:
            return ''

def id_chenk_X(s_id: str) -> str:
    """
    获取身份证校验位*免责声明:仅供学习参考禁止违法犯罪
    """
    if len(s_id) == 18:
        s = s_id[:17]
    elif len(s_id) == 17:
        s = s_id
    else:
        return False
    x = ['1','0','X','9','8','7','6','5','4','3','2']
    val = 0
    for i in range(17,0,-1):
        # print(s[17 - i])
        val += (pow(2,i) % 11) * int(s[17 - i])
    return x[val % 11]

def chenk_id(s_id: str) -> bool:
    """
    检查身份证是否合法*免责声明:仅供学习参考禁止违法犯罪
    """
    if len(s_id) != 18:
        return False
    return id_chenk_X(s_id) == s_id[17]

def id_analysis(s_id: str) -> dict:
    """
    取身份证信息*免责声明:仅供学习参考禁止违法犯罪
    """
    if not chenk_id(s_id):
        return False
    s = js.get(s_id[0:2] + '0000','')
    shi = js.get(s_id[0:4] + '00','')
    qu = js.get(s_id[0:6],'')
    if s == '':
        region = get(s_id[0:6])
    elif shi == '':
        region = get(s_id[0:6])
    elif qu == '':
        region = get(s_id[0:6])
    else:
        region = s + shi + qu
    if (int(s_id[16]) % 2) == 1:
        gender = 'boy'
    else:
        gender = 'girl'
    return {'status':region != '','id':s_id,'region':region,'gender':gender,'birthday':s_id[6:14]}

def rand_id(year: int) -> str:
    """
    生成指定岁数随机身份证*免责声明:仅供学习参考禁止违法犯罪
    """
    rand = random.randint(0,len(js))
    n = 0
    for i in js:
        if n == rand:
            rand = str(random.randint(100,999))
            stime = str(datetime.datetime.now().year - year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day)
            return i + stime + rand + id_chenk_X(i + stime + rand)
        n += 1

# print(id_analysis(rand_id(18)))
