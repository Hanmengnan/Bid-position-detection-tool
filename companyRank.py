from json import loads
from lxml import etree
import re
from fun import fun
class rank:
    def _init_(self):
        return 
    def search(self,keyword):
        try:
            html=fun(keyword)
            htmls=etree.HTML(html)
            fonts=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*/span/a/@data-renzheng")#定位
            website=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*/a/span[1]/text()")
            url=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*/a/@href")
            self.title=[] #公司名字
            self.web=[] #公司网址
            for i in website:
                self.web.append(i)
            for i in fonts:
                self.title.append(loads(i)['title'])
        except:
            self.title=[]
            self.web=[]
    def search_name(self,data):
        if data in self.web:
            return self.web.index(data)
        else:
            for i in self.title:
                if not re.search(data,i)==None:
                    return self.title.index(i)

    def main(self,keyword,website):
        self.search(keyword)
        result=self.search_name(website)
        if result==None:
            return None
        else :
            return result+1

