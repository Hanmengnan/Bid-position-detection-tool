import requests
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}
def fun(keyword):
    url=("https://www.baidu.com/s?ie=UTF-8&wd=%s"%(keyword))#网址
    html=requests.get(url,headers=headers , timeout=(3,7)).text
    s = requests.session()
    s.keep_alive =False#防止源代码过长，超时导致SSL错误
    return html