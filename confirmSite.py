from json import loads
from fun import *
from lxml import etree
def search(keyword):
    comState={}
    html=fun(keyword)
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
if __name__=="__main__":
    print(search(1))