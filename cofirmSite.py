import requests
from lxml import etree
from json import loads
from fun import *
class comfirmSite():
    def search(keyword):
        comState={}
        html=fun("灭火器")
        htmls=etree.HTML(html)
        htmls=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*")
        for each in htmls:
            url=each.xpath("./a/@href")[0]
            code = requests.get(url, headers=headers).status_code
            company=each.xpath("./span/a/@data-renzheng")[0]
            if code != requests.codes.ok:
                comState[loads(company)['title']]=True
            else:
                comState[loads(company)['title']] = False
        return comState