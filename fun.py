import requests
from json import loads
from lxml import etree
import re
class rank:
    def _init_(self):
        return 
    def search_web(self,keyword):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}
            
            url=("https://www.baidu.com/s?ie=UTF-8&wd=%s"%(keyword))#网址

            html=requests.get(url,headers=headers , timeout=(3,7)).text

            s = requests.session()
            s.keep_alive =False#防止源代码过长，超时导致SSL错误

            htmls=etree.HTML(html)

            fonts=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*/span/a/@data-renzheng")#定位
            website=htmls.xpath("//*[contains(@class,'ec_tuiguang_container')]/parent::*/a/span[1]/text()")
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
        self.search_web(keyword)
        result=self.search_name(website)
        if result==None:
            return None
        else :
            return result+1

