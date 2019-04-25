

import requests
from lxml import etree
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}
def fun(keyword):
    url=("https://bj.58.com/huangyezonghe/?key=%s&cmcskey=%s&final=1&jump=1&specialtype=gls&classpolicy=huangyezonghe_Bs"%(keyword,keyword))#网址
    html=requests.get(url,headers=headers , timeout=(3,7)).text
    s = requests.session()
    s.keep_alive =False#防止源代码过长，超时导致SSL错误
    html=etree.HTML(html)
    jingpinBox=html.xpath("//*[@class='jingpin']/parent::*/parent::*/p[1]/a")
    dingzhiBox=html.xpath("//*[@class='ico ding']/parent::*/parent::*/p[1]/a")
    totalBox=html.xpath("//*[@class='seller']/a")
    jingpin=[]
    dingzhi=[]
    other=[]
    for i in jingpinBox:
        if i!=None:
            jingpin.append(i.text)
    for i in dingzhiBox:
        if i!=None:
            dingzhi.append(i.text)
    for i in range(len(totalBox)-len(dingzhiBox)-len(jingpinBox)):
        if i!=None:
            other.append(totalBox[len(dingzhiBox)+len(jingpinBox)-1+i].text)

